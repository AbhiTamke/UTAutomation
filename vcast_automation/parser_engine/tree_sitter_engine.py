from __future__ import annotations

import logging
from typing import Any, Optional

from vcast_automation.parser_engine.body_structure import parse_block
from vcast_automation.parser_engine.code_model import (
    CallInfo,
    CallType,
    ControlConstruct,
    EnumInfo,
    FunctionInfo,
    IncludeInfo,
    ParsedFile,
    StructInfo,
    SwitchCase,
)
from vcast_automation.parser_engine.lightweight_c_parser import (
    _normalize_return_type,
    _parse_parameters,
    _render_signature,
)
from vcast_automation.parser_engine.parser_base import ParserBase

logger = logging.getLogger(__name__)


def _try_load_languages():
    """
    Return C and C++ tree-sitter languages if available.

    First tries tree_sitter_languages.
    Then tries a manually built shared library from EA_SDD_TREE_SITTER_LIB.
    If neither works, returns (None, None).
    """
    try:
        from tree_sitter_languages import get_language  # type: ignore

        return get_language("c"), get_language("cpp")
    except Exception:
        pass

    try:
        from tree_sitter import Language  # type: ignore
        import os

        lib = os.environ.get("EA_SDD_TREE_SITTER_LIB")

        if lib and os.path.isfile(lib):
            return Language(lib, "c"), Language(lib, "cpp")
    except Exception:
        pass

    return None, None


class TreeSitterEngine(ParserBase):
    """
    Optional high-fidelity parser backed by tree-sitter.

    This parser is optional. If tree_sitter or the grammars are unavailable,
    available() returns False and ParserSelector should fall back to
    LightweightCParser.
    """

    name = "tree_sitter"

    def __init__(self) -> None:
        self._parser_c: Optional[Any] = None
        self._parser_cpp: Optional[Any] = None
        self._loaded = False
        self._available = False

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return

        self._loaded = True

        try:
            from tree_sitter import Parser  # type: ignore
        except Exception:
            logger.info("tree_sitter is not installed; primary parser unavailable.")
            self._available = False
            return

        c_language, cpp_language = _try_load_languages()

        if c_language is None:
            logger.info("tree-sitter C grammar unavailable; primary parser disabled.")
            self._available = False
            return

        try:
            self._parser_c = Parser()

            if hasattr(self._parser_c, "set_language"):
                self._parser_c.set_language(c_language)
            else:
                self._parser_c.language = c_language

            if cpp_language is not None:
                self._parser_cpp = Parser()

                if hasattr(self._parser_cpp, "set_language"):
                    self._parser_cpp.set_language(cpp_language)
                else:
                    self._parser_cpp.language = cpp_language

            self._available = True
            logger.info("tree-sitter parser engine is available.")

        except Exception as exc:
            logger.warning("Failed to initialize tree-sitter parser: %s", exc)
            self._available = False

    def available(self) -> bool:
        self._ensure_loaded()
        return self._available

    def _select_parser(self, path: str):
        lower = path.lower()

        if lower.endswith((".cpp", ".hpp", ".cc", ".cxx", ".hh", ".hxx")) and self._parser_cpp:
            return self._parser_cpp

        return self._parser_c

    def parse_text(self, path: str, text: str, is_header: bool) -> ParsedFile:
        pf = ParsedFile(path=path, is_header=is_header, parser_used=self.name)

        if not self.available():
            pf.parse_ok = False
            pf.warnings.append("tree-sitter unavailable")
            return pf

        try:
            parser = self._select_parser(path)

            if parser is None:
                pf.parse_ok = False
                pf.warnings.append("tree-sitter parser object is unavailable")
                return pf

            tree = parser.parse(bytes(text, "utf-8"))

        except Exception as exc:
            pf.parse_ok = False
            pf.warnings.append(f"tree-sitter parse failed: {exc}")
            return pf

        source = bytes(text, "utf-8")

        try:
            self._walk(tree.root_node, source, path, pf)
        except Exception as exc:
            pf.parse_ok = False
            pf.warnings.append(f"tree-sitter AST walk failed: {exc}")

        return pf

    def _text(self, node: Any, source: bytes) -> str:
        if node is None:
            return ""

        return source[node.start_byte:node.end_byte].decode("utf-8", "replace")

    def _walk(self, node: Any, source: bytes, path: str, pf: ParsedFile) -> None:
        for child in node.children:
            node_type = child.type

            if node_type == "function_definition":
                fn = self._function(child, source, path)

                if fn:
                    pf.functions.append(fn)

            elif node_type == "preproc_include":
                include = self._include(child, source, path)

                if include:
                    pf.includes.append(include)

            elif node_type == "enum_specifier":
                enum = self._enum(child, source, path)

                if enum:
                    pf.enums.append(enum)

            elif node_type in {"struct_specifier", "union_specifier"}:
                struct = self._struct(child, source, path)

                if struct:
                    pf.structs.append(struct)

            else:
                self._walk(child, source, path, pf)

    def _include(self, node: Any, source: bytes, path: str) -> Optional[IncludeInfo]:
        raw = self._text(node, source)
        is_system = "<" in raw

        if is_system:
            target = raw.split("<")[-1].split(">")[0]
        else:
            parts = raw.split('"')
            target = parts[1] if len(parts) > 1 else raw

        return IncludeInfo(
            target=str(target).strip(),
            is_system=is_system,
            file_path=path,
            line_number=node.start_point[0] + 1,
        )

    def _enum(self, node: Any, source: bytes, path: str) -> Optional[EnumInfo]:
        name_node = node.child_by_field_name("name")
        name = self._text(name_node, source) if name_node else f"AnonymousEnum_{node.start_point[0] + 1}"

        values: list[str] = []
        body = node.child_by_field_name("body")

        if body:
            for child in body.children:
                if child.type == "enumerator":
                    enum_name = child.child_by_field_name("name")

                    if enum_name:
                        values.append(self._text(enum_name, source))

        return EnumInfo(
            name=name,
            values=values,
            file_path=path,
            line_number=node.start_point[0] + 1,
        )

    def _struct(self, node: Any, source: bytes, path: str) -> Optional[StructInfo]:
        name_node = node.child_by_field_name("name")

        if not name_node:
            return None

        return StructInfo(
            name=self._text(name_node, source),
            kind="union" if node.type == "union_specifier" else "struct",
            file_path=path,
            line_number=node.start_point[0] + 1,
        )

    def _function(self, node: Any, source: bytes, path: str) -> Optional[FunctionInfo]:
        declarator = node.child_by_field_name("declarator")
        raw_name = self._declarator_name(declarator, source) if declarator else None

        if not raw_name:
            return None

        function_name = raw_name.split("::")[-1]

        type_node = node.child_by_field_name("type")
        return_type = _normalize_return_type(self._text(type_node, source)) if type_node else "void"

        params_text = self._params_text(declarator, source)
        body_node = node.child_by_field_name("body")
        body_text = self._text(body_node, source) if body_node else ""

        fn = FunctionInfo(
            name=function_name,
            qualified_name=raw_name,
            signature=_render_signature(return_type, raw_name, params_text),
            return_type=return_type or "void",
            parameters=_parse_parameters(params_text),
            file_path=path,
            line_start=node.start_point[0] + 1,
            line_end=node.end_point[0] + 1,
            is_static="static" in self._text(node, source).split("{")[0].split(),
            body=body_text,
            parser_confidence="high",
        )

        if body_node:
            self._analyze_body(fn, body_node, source)

        if body_text:
            try:
                fn.body_block = parse_block(body_text, base_line=fn.line_start)
            except Exception as exc:
                fn.assumptions.append(f"Structured body parse failed: {exc}")

        return fn

    def _declarator_name(self, node: Any, source: bytes) -> Optional[str]:
        """
        Extract function name from tree-sitter declarator nodes.

        Handles common C/C++ forms:
        - identifier
        - function_declarator
        - pointer_declarator
        - reference_declarator
        - qualified_identifier / scoped_identifier-like text
        """
        if node is None:
            return None

        node_type = getattr(node, "type", "")

        if node_type == "identifier":
            return self._text(node, source)

        if node_type in {"qualified_identifier", "scoped_identifier", "field_identifier"}:
            return self._text(node, source).replace(" ", "")

        name_field = node.child_by_field_name("name")
        if name_field is not None:
            name_text = self._text(name_field, source).replace(" ", "")
            if name_text:
                return name_text

        declarator_field = node.child_by_field_name("declarator")
        if declarator_field is not None:
            found = self._declarator_name(declarator_field, source)
            if found:
                return found

        for child in node.children:
            child_type = getattr(child, "type", "")

            if child_type in {"identifier", "qualified_identifier", "scoped_identifier", "field_identifier"}:
                text = self._text(child, source).replace(" ", "")
                if text:
                    return text

        for child in node.children:
            if getattr(child, "type", "").endswith("declarator"):
                found = self._declarator_name(child, source)
                if found:
                    return found

        return None

    def _params_text(self, declarator: Any, source: bytes) -> str:
        if declarator is None:
            return ""

        stack = [declarator]

        while stack:
            current = stack.pop()

            if current is None:
                continue

            if current.type == "parameter_list":
                inner = self._text(current, source).strip()
                return inner[1:-1] if inner.startswith("(") and inner.endswith(")") else inner

            stack.extend(current.children)

        return ""

    def _analyze_body(self, fn: FunctionInfo, body: Any, source: bytes) -> None:
        local_names = {parameter.name for parameter in fn.parameters}

        def visit(node: Any) -> None:
            node_type = node.type

            if node_type == "call_expression":
                function_node = node.child_by_field_name("function")

                if function_node is not None:
                    callee = self._text(function_node, source).replace(" ", "")

                    if callee and callee not in local_names:
                        fn.calls.append(
                            CallInfo(
                                caller=fn.name,
                                callee=callee,
                                call_type=CallType.UNRESOLVED,
                                line_number=node.start_point[0] + 1,
                            )
                        )

            elif node_type == "if_statement":
                cond = node.child_by_field_name("condition")
                cond_text = self._text(cond, source) if cond else ""

                cc = ControlConstruct(
                    kind="if",
                    condition=cond_text,
                    line_number=node.start_point[0] + 1,
                    summary=f"Decision: {cond_text}" if cond_text else "Decision",
                )

                fn.control_constructs.append(cc)
                fn.conditions.append(cc)

            elif node_type in {"for_statement", "while_statement", "do_statement"}:
                kind = node_type.split("_")[0]
                cond = node.child_by_field_name("condition")
                cond_text = self._text(cond, source) if cond else ""

                cc = ControlConstruct(
                    kind=kind,
                    condition=cond_text,
                    line_number=node.start_point[0] + 1,
                    summary=f"Loop while {cond_text}" if cond_text else "Loop",
                )

                fn.control_constructs.append(cc)
                fn.loops.append(cc)

            elif node_type == "switch_statement":
                cond = node.child_by_field_name("condition")
                cond_text = self._text(cond, source) if cond else ""

                fn.control_constructs.append(
                    ControlConstruct(
                        kind="switch",
                        condition=cond_text,
                        line_number=node.start_point[0] + 1,
                        summary=f"Switch on {cond_text}" if cond_text else "Switch",
                    )
                )

                for child in self._descendants(node):
                    if child.type == "case_statement":
                        label_node = child.child_by_field_name("value")

                        if label_node is not None:
                            fn.switch_cases.append(
                                SwitchCase(label=self._text(label_node, source))
                            )

                    elif child.type == "default_statement":
                        fn.switch_cases.append(
                            SwitchCase(label="default", is_default=True)
                        )

            elif node_type == "return_statement":
                fn.return_paths += 1

            for child in node.children:
                visit(child)

        visit(body)

    def _descendants(self, node: Any):
        for child in node.children:
            yield child
            yield from self._descendants(child)