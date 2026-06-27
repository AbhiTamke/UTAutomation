from __future__ import annotations

from pathlib import Path

from vcast_automation.diagnostics.codes import (
    PARSER_CPP_QUALIFICATION_LOW_CONFIDENCE,
    PARSER_LIGHTWEIGHT_FALLBACK_USED,
)
from vcast_automation.models.core import (
    ConditionModel,
    Diagnostic,
    FunctionModel,
    LoopModel,
    ParameterModel,
    SourceFileModel,
    SwitchCaseModel,
)
from vcast_automation.parser_engine.code_model import ParsedFile


def language_for_path(path: str) -> str:
    suffix = Path(path).suffix.lower()
    if suffix in {".cpp", ".hpp", ".cc", ".cxx", ".hh", ".hxx"}:
        return "cpp"
    if suffix in {".c", ".h"}:
        return "c"
    return "unknown"


def resolve_vcast_subprogram_name(qualified_name: str, function_name: str) -> tuple[str, str, list[Diagnostic]]:
    """
    Conservative C++ resolver.

    If class qualification is proven as A::B::method, VectorCAST style becomes:
    (cl)B::method

    Otherwise, use the plain function name.
    """
    diagnostics: list[Diagnostic] = []
    parts = [part.strip() for part in qualified_name.split("::") if part.strip()]

    if len(parts) >= 2:
        return f"(cl){parts[-2]}::{parts[-1]}", "medium", diagnostics

    diagnostics.append(
        Diagnostic(
            code=PARSER_CPP_QUALIFICATION_LOW_CONFIDENCE,
            message="C++ class qualification was not proven; using unqualified subprogram name.",
        )
    )
    return function_name, "low", diagnostics


def map_parsed_file_to_source_model(parsed: ParsedFile) -> SourceFileModel:
    path = Path(parsed.path)
    unit_name = path.stem

    source = SourceFileModel(
        source_path=parsed.path,
        source_stem=path.stem,
        unit_name=unit_name,
        language=language_for_path(parsed.path),
        parser_backend=parsed.parser_used,
        parser_confidence="high" if parsed.parser_used == "tree_sitter" else "medium",
    )

    if parsed.parser_used == "lightweight":
        source.diagnostics.append(
            Diagnostic(
                code=PARSER_LIGHTWEIGHT_FALLBACK_USED,
                message="Lightweight parser backend used.",
                source=parsed.path,
            )
        )

    for warning in parsed.warnings:
        source.diagnostics.append(
            Diagnostic(
                code="PARSER_WARNING",
                message=warning,
                source=parsed.path,
            )
        )

    for fn in parsed.functions:
        subprogram, qualification_confidence, diagnostics = resolve_vcast_subprogram_name(
            fn.qualified_name,
            fn.name,
        )

        parameters = [
            ParameterModel(
                name=p.name,
                type=p.type,
                is_pointer=p.is_pointer,
                is_reference=p.is_reference,
                is_const=p.is_const,
                is_array=p.is_array,
                # Extended fields for richer analysis
                base_type=_infer_base_type(p.type),
                pointer_depth=_count_pointer_depth(p.is_pointer, p.type),
            )
            for p in fn.parameters
            if p.name
        ]

        conditions = [
            ConditionModel(
                expression=c.condition,
                kind=c.kind,
                line_start=c.line_number,
                parser_confidence=fn.parser_confidence,
            )
            for c in fn.conditions
        ]

        loops = [
            LoopModel(
                kind=l.kind,
                condition=l.condition,
                line_number=l.line_number,
            )
            for l in fn.loops
        ]

        switch_cases = [
            SwitchCaseModel(
                label=s.label,
                is_default=s.is_default,
            )
            for s in fn.switch_cases
        ]

        function_model = FunctionModel(
            source_path=parsed.path,
            unit_name=unit_name,
            function_name=fn.name,
            qualified_name=fn.qualified_name,
            vcast_subprogram_name=subprogram,
            return_type=fn.return_type,
            signature=fn.signature,
            parameters=parameters,
            conditions=conditions,
            loops=loops,
            switch_cases=switch_cases,
            return_paths=fn.return_paths,
            line_start=fn.line_start,
            line_end=fn.line_end,
            is_static=fn.is_static,
            parser_backend=parsed.parser_used,
            parser_confidence=fn.parser_confidence,
            qualification_confidence=qualification_confidence,
            diagnostics=diagnostics,
            # Extended fields for analysis
            globals_read=getattr(fn, 'globals_read', []),
            globals_written=getattr(fn, 'globals_written', []),
            calls=getattr(fn, 'calls', []),
            internal_calls=getattr(fn, 'internal_calls', []),
            external_calls=getattr(fn, 'external_calls', []),
        )

        # Post-process to extract constraints and infer dependencies
        try:
            from vcast_automation.parser_engine.constraint_extractor import (
                extract_simple_constraints,
                extract_condition_targets,
                tag_potentially_unreachable,
            )

            # Extract constraints from conditions
            constraints = extract_simple_constraints(function_model)
            
            # Tag unreachable code
            unreachable_diagnostics = tag_potentially_unreachable(function_model)
            function_model.diagnostics.extend(unreachable_diagnostics)
            
            # Infer parameter dependencies
            function_model.input_dependencies = _infer_input_dependencies(
                function_model, constraints
            )
        except Exception as exc:
            # Gracefully skip constraint extraction if it fails
            function_model.diagnostics.append(
                Diagnostic(
                    code="CONSTRAINT_EXTRACTION_ERROR",
                    message=f"Constraint extraction failed: {exc}",
                    severity="warning",
                )
            )

        source.functions.append(function_model)

    return source


# Helper functions for constraint extraction and dependency inference

def _infer_base_type(type_str: str) -> str:
    """Extract base type from pointer/array notation."""
    base = type_str.replace("*", "").replace("[]", "").replace("&", "").strip()
    return base


def _count_pointer_depth(is_pointer: bool, type_str: str) -> int:
    """Count the depth of pointer indirection."""
    if not is_pointer:
        return 0
    # Simple count of * in type string
    return type_str.count("*")


def _infer_input_dependencies(function_model: FunctionModel, constraints: dict) -> list[dict]:
    """
    Infer parameter input dependencies from naming patterns and constraints.
    
    Detects:
    - Size/buffer pairs (array_size -> array)
    - Pointer validity flags (ptr -> is_valid_ptr)
    - Output parameters (out_* patterns)
    """
    dependencies = []
    param_names = {p.name for p in function_model.parameters}
    
    for param in function_model.parameters:
        dep_list = []
        
        # Size/buffer detection
        if _is_size_like(param.name):
            for other in function_model.parameters:
                if _is_buffer_like(other.name) and _names_match_pair(param.name, other.name):
                    dep_list.append({
                        "type": "size_of",
                        "target": other.name,
                        "confidence": "high" if other.is_pointer or other.is_array else "medium",
                    })
        
        # Validity flag detection
        if _is_validity_flag(param.name):
            for other in function_model.parameters:
                if other.is_pointer and _names_match_pair(param.name, other.name):
                    dep_list.append({
                        "type": "validity_flag_for",
                        "target": other.name,
                        "confidence": "medium",
                    })
        
        if dep_list:
            dependencies.append({
                "parameter": param.name,
                "dependencies": dep_list,
            })
    
    return dependencies


def _is_size_like(name: str) -> bool:
    """Check if name suggests a size/length parameter."""
    lower = name.lower()
    return any(
        hint in lower
        for hint in ("size", "length", "len", "count", "num", "nelem", "n_", "nbytes")
    )


def _is_buffer_like(name: str) -> bool:
    """Check if name suggests a buffer/array parameter."""
    lower = name.lower()
    return any(
        hint in lower
        for hint in ("buf", "array", "data", "ptr", "p_", "buffer", "arr")
    )


def _is_validity_flag(name: str) -> bool:
    """Check if name suggests a validity/allocated flag."""
    lower = name.lower()
    return any(
        hint in lower
        for hint in ("valid", "allocated", "is_valid", "is_allocated", "allocated_", "valid_")
    )


def _names_match_pair(size_name: str, buffer_name: str) -> bool:
    """Check if size and buffer names are related."""
    # Remove common affixes and compare what's left
    size_stem = size_name.lower().replace("size", "").replace("length", "").replace("len", "").replace("count", "").replace("_", "")
    buffer_stem = buffer_name.lower().replace("buf", "").replace("buffer", "").replace("data", "").replace("ptr", "").replace("p_", "").replace("array", "").replace("arr", "").replace("_", "")
    
    # Direct substring match or very similar
    return size_stem in buffer_stem or buffer_stem in size_stem or len(size_stem) < 3 or len(buffer_stem) < 3