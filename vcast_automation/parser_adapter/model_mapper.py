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
        )

        source.functions.append(function_model)

    return source