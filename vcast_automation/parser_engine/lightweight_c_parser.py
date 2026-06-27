from __future__ import annotations

import logging
import re
from typing import Optional

from vcast_automation.parser_engine.body_structure import parse_block
from vcast_automation.parser_engine.code_model import (
    CallInfo,
    CallType,
    ControlConstruct,
    EnumInfo,
    FunctionInfo,
    IncludeInfo,
    ParameterInfo,
    ParsedFile,
    PreprocessorBlock,
    StructInfo,
    SwitchCase,
    TypedefInfo,
    VariableInfo,
)
from vcast_automation.parser_engine.parser_base import ParserBase

logger = logging.getLogger(__name__)


# C/C++ keywords that may appear before "(" but are not normal function calls.
_CONTROL_KEYWORDS = {
    "if",
    "for",
    "while",
    "switch",
    "return",
    "sizeof",
    "defined",
    "do",
    "else",
    "case",
    "default",
    "static_cast",
    "reinterpret_cast",
    "const_cast",
    "dynamic_cast",
}

_TYPE_QUALIFIERS = {
    "static",
    "inline",
    "extern",
    "const",
    "volatile",
    "register",
    "FUNC",
    "STATIC",
    "INLINE",
    "LOCAL_INLINE",
}

# Function definition:
# optional qualifiers/return type, function name, parameter list, then "{"
#
# Supports simple C names:
#   int foo(int a) {
#
# Supports visible C++ qualified names:
#   int ClassName::foo(int a) {
#
# Note:
# This is not a full C++ parser. It is a pragmatic fallback parser.
_FUNC_HEADER_RE = re.compile(
    r"(?P<head>[A-Za-z_][\w\s\*\&:<>,~]*?)\b"
    r"(?P<name>[A-Za-z_~]\w*(?:::\s*[A-Za-z_~]\w*)*)\s*"
    r"\((?P<params>[^;{}]*)\)\s*"
    r"(?P<suffix>(?:const|noexcept|override|final|\s)*)\{",
    re.MULTILINE,
)

# Function declaration/prototype:
#   int foo(int a);
_FUNC_DECL_RE = re.compile(
    r"(?P<head>[A-Za-z_][\w\s\*\&:<>,~]*?)\b"
    r"(?P<name>[A-Za-z_~]\w*(?:::\s*[A-Za-z_~]\w*)*)\s*"
    r"\((?P<params>[^;{}]*)\)\s*;",
    re.MULTILINE,
)

_CALL_RE = re.compile(r"\b(?P<name>[A-Za-z_]\w*)\s*\(")

_INCLUDE_RE = re.compile(
    r'^\s*#\s*include\s*(?P<q>["<])(?P<target>[^">]+)[">]',
    re.MULTILINE,
)

_DEFINE_RE = re.compile(
    r"^\s*#\s*define\s+"
    r"(?P<name>[A-Za-z_]\w*)"
    r"(?P<args>\([^)]*\))?"
    r"\s*(?P<value>.*)$",
    re.MULTILINE,
)

_PREPROC_COND_RE = re.compile(
    r"^\s*#\s*(?P<kind>if|ifdef|ifndef|elif|else|endif)\b(?P<expr>.*)$"
)

_ENUM_RE = re.compile(
    r"\benum\s+(?:class\s+|struct\s+)?(?P<name>[A-Za-z_]\w*)?\s*"
    r"(?::\s*[\w:\s]+?)?\s*"
    r"\{(?P<body>[^}]*)\}\s*"
    r"(?P<alias>[A-Za-z_]\w*)?\s*;",
    re.MULTILINE,
)

_STRUCT_RE = re.compile(
    r"\b(?P<kind>struct|union)\s+"
    r"(?P<name>[A-Za-z_]\w*)\s*"
    r"\{(?P<body>[^{}]*)\}",
    re.MULTILINE,
)

_TYPEDEF_SIMPLE_RE = re.compile(
    r"\btypedef\s+"
    r"(?P<underlying>[\w\s\*]+?)\s+"
    r"(?P<name>[A-Za-z_]\w*)\s*;",
    re.MULTILINE,
)


def _strip_comments_and_strings(text: str) -> str:
    """
    Replace comments and string/char literals with spaces, preserving newlines.

    This keeps line numbers and brace structure mostly intact while removing
    braces/parentheses that may appear inside comments or literals.
    """
    out: list[str] = []
    i = 0
    state = "code"

    while i < len(text):
        ch = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ""

        if state == "code":
            if ch == "/" and nxt == "/":
                state = "line_comment"
                out.append("  ")
                i += 2
                continue

            if ch == "/" and nxt == "*":
                state = "block_comment"
                out.append("  ")
                i += 2
                continue

            if ch == '"':
                state = "string"
                out.append(" ")
                i += 1
                continue

            if ch == "'":
                state = "char"
                out.append(" ")
                i += 1
                continue

            out.append(ch)
            i += 1
            continue

        if state == "line_comment":
            if ch == "\n":
                state = "code"
                out.append("\n")
            else:
                out.append(" ")
            i += 1
            continue

        if state == "block_comment":
            if ch == "*" and nxt == "/":
                state = "code"
                out.append("  ")
                i += 2
                continue

            out.append("\n" if ch == "\n" else " ")
            i += 1
            continue

        if state == "string":
            if ch == "\\":
                out.append("  ")
                i += 2
                continue

            if ch == '"':
                state = "code"

            out.append("\n" if ch == "\n" else " ")
            i += 1
            continue

        if state == "char":
            if ch == "\\":
                out.append("  ")
                i += 2
                continue

            if ch == "'":
                state = "code"

            out.append("\n" if ch == "\n" else " ")
            i += 1
            continue

    return "".join(out)


def _strip_preprocessor_lines(text: str) -> str:
    """
    Replace preprocessor directive lines with spaces, preserving newlines.

    Includes and macros are extracted from original text before this function is
    used. Function-like macros can otherwise look like function definitions.
    """
    cleaned: list[str] = []

    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()

        if stripped.startswith("#"):
            newline = "\n" if line.endswith("\n") else ""
            cleaned.append(" " * (len(line) - len(newline)) + newline)
        else:
            cleaned.append(line)

    return "".join(cleaned)


def _line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def _match_brace(text: str, open_index: int) -> int:
    """
    Return the index just after the matching closing brace.

    If braces are unbalanced, return len(text), allowing the parser to continue
    conservatively.
    """
    depth = 0
    i = open_index

    while i < len(text):
        ch = text[i]

        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1

            if depth == 0:
                return i + 1

        i += 1

    return len(text)


def _active_preprocessor_conditions(text: str, target_line: int) -> list[str]:
    """
    Return active preprocessor conditions before target_line.
    """
    stack: list[str] = []

    for line_no, line in enumerate(text.splitlines(), start=1):
        if line_no >= target_line:
            break

        match = _PREPROC_COND_RE.match(line)
        if not match:
            continue

        kind = match.group("kind")
        expr = (match.group("expr") or "").strip()

        if kind == "ifdef":
            stack.append(f"defined({expr})" if expr else "defined(?)")
        elif kind == "ifndef":
            stack.append(f"!defined({expr})" if expr else "!defined(?)")
        elif kind == "if":
            stack.append(expr or "#if")
        elif kind == "elif":
            if stack:
                stack[-1] = expr or "#elif"
            else:
                stack.append(expr or "#elif")
        elif kind == "else":
            if stack:
                stack[-1] = f"else({stack[-1]})"
            else:
                stack.append("#else")
        elif kind == "endif":
            if stack:
                stack.pop()

    return list(stack)


def _preprocessor_blocks(text: str, start_line: int, end_line: int) -> list[PreprocessorBlock]:
    """
    Return preprocessor conditional blocks inside a function line range.
    """
    blocks: list[PreprocessorBlock] = []
    stack: list[tuple[str, int]] = []

    for line_no, line in enumerate(text.splitlines(), start=1):
        if line_no < start_line:
            continue

        if line_no > end_line:
            break

        match = _PREPROC_COND_RE.match(line)
        if not match:
            continue

        kind = match.group("kind")
        expr = (match.group("expr") or "").strip()

        if kind in {"if", "ifdef", "ifndef"}:
            if kind == "ifdef":
                condition = f"defined({expr})" if expr else "defined(?)"
            elif kind == "ifndef":
                condition = f"!defined({expr})" if expr else "!defined(?)"
            else:
                condition = expr or "#if"

            stack.append((condition, line_no + 1))

        elif kind in {"elif", "else"}:
            previous_condition = ""

            if stack:
                previous_condition, block_start = stack.pop()

                if block_start <= line_no - 1:
                    blocks.append(
                        PreprocessorBlock(
                            condition=previous_condition,
                            line_start=block_start,
                            line_end=line_no - 1,
                        )
                    )

            if kind == "elif":
                stack.append((expr or "#elif", line_no + 1))
            else:
                stack.append(
                    (
                        f"else({previous_condition})" if previous_condition else "#else",
                        line_no + 1,
                    )
                )

        elif kind == "endif":
            if stack:
                condition, block_start = stack.pop()

                if block_start <= line_no - 1:
                    blocks.append(
                        PreprocessorBlock(
                            condition=condition,
                            line_start=block_start,
                            line_end=line_no - 1,
                        )
                    )

    while stack:
        condition, block_start = stack.pop()

        if block_start <= end_line:
            blocks.append(
                PreprocessorBlock(
                    condition=condition,
                    line_start=block_start,
                    line_end=end_line,
                )
            )

    return blocks


class LightweightCParser(ParserBase):
    """
    Regex + brace-matching parser used as the always-available fallback.

    It extracts:
    - includes
    - macros
    - enums
    - structs/unions
    - typedefs
    - globals
    - function definitions
    - function declarations/prototypes
    - parameters
    - calls
    - conditions
    - loops
    - switch/case/default
    - return paths
    - structured body blocks
    """

    name = "lightweight"

    def available(self) -> bool:
        return True

    def parse_text(self, path: str, text: str, is_header: bool) -> ParsedFile:
        pf = ParsedFile(path=path, is_header=is_header, parser_used=self.name)

        try:
            sanitized = _strip_preprocessor_lines(_strip_comments_and_strings(text))
        except Exception as exc:
            pf.parse_ok = False
            pf.warnings.append(f"Comment/string stripping failed: {exc}")
            sanitized = text

        self._extract_includes(text, path, pf)
        self._extract_macros(text, path, pf)
        self._extract_enums(sanitized, path, pf)
        self._extract_structs(sanitized, path, pf)
        self._extract_typedefs(sanitized, path, pf)

        function_spans = self._extract_functions(sanitized, text, path, pf)
        self._extract_globals(sanitized, path, pf, function_spans)

        return pf

    def _extract_includes(self, text: str, path: str, pf: ParsedFile) -> None:
        for match in _INCLUDE_RE.finditer(text):
            pf.includes.append(
                IncludeInfo(
                    target=match.group("target").strip(),
                    is_system=match.group("q") == "<",
                    file_path=path,
                    line_number=_line_of(text, match.start()),
                )
            )

    def _extract_macros(self, text: str, path: str, pf: ParsedFile) -> None:
        for match in _DEFINE_RE.finditer(text):
            value = (match.group("value") or "").strip()
            is_const_like = match.group("args") is None and value != ""

            pf.macros.append(
                VariableInfo(
                    name=match.group("name"),
                    type="macro",
                    is_macro=True,
                    is_const=is_const_like,
                    initial_value=value,
                    file_path=path,
                    line_number=_line_of(text, match.start()),
                )
            )

    def _extract_enums(self, text: str, path: str, pf: ParsedFile) -> None:
        for match in _ENUM_RE.finditer(text):
            name = match.group("name") or match.group("alias")

            if not name:
                name = f"AnonymousEnum_{_line_of(text, match.start())}"

            values: list[str] = []

            for token in match.group("body").split(","):
                token = token.strip()

                if not token:
                    continue

                value_name = token.split("=")[0].strip()

                if value_name:
                    values.append(value_name)

            pf.enums.append(
                EnumInfo(
                    name=name,
                    values=values,
                    file_path=path,
                    line_number=_line_of(text, match.start()),
                )
            )

    def _extract_structs(self, text: str, path: str, pf: ParsedFile) -> None:
        for match in _STRUCT_RE.finditer(text):
            fields: list[ParameterInfo] = []

            for raw in match.group("body").split(";"):
                raw = raw.strip()

                if not raw:
                    continue

                parsed = _parse_declarator(raw)

                if parsed:
                    fields.append(parsed)

            pf.structs.append(
                StructInfo(
                    name=match.group("name"),
                    kind=match.group("kind"),
                    fields=fields,
                    file_path=path,
                    line_number=_line_of(text, match.start()),
                )
            )

    def _extract_typedefs(self, text: str, path: str, pf: ParsedFile) -> None:
        for match in _TYPEDEF_SIMPLE_RE.finditer(text):
            pf.typedefs.append(
                TypedefInfo(
                    name=match.group("name"),
                    underlying_type=match.group("underlying").strip(),
                    file_path=path,
                    line_number=_line_of(text, match.start()),
                )
            )

    def _extract_functions(
        self,
        sanitized: str,
        original: str,
        path: str,
        pf: ParsedFile,
    ) -> list[tuple[int, int]]:
        spans: list[tuple[int, int]] = []
        consumed_decl_ranges: list[tuple[int, int]] = []
        pos = 0

        while True:
            match = _FUNC_HEADER_RE.search(sanitized, pos)

            if not match:
                break

            brace_open = sanitized.find("{", match.end() - 1)

            if brace_open == -1:
                break

            body_end = _match_brace(sanitized, brace_open)
            head = match.group("head").strip()
            raw_name = re.sub(r"\s+", "", match.group("name"))
            function_name = raw_name.split("::")[-1]
            params = match.group("params").strip()

            if function_name in _CONTROL_KEYWORDS or not head:
                pos = body_end
                continue

            return_type = _normalize_return_type(head)

            if not return_type:
                pos = body_end
                continue

            body = sanitized[brace_open:body_end]
            line_start = _line_of(sanitized, match.start())
            line_end = _line_of(sanitized, body_end)

            fn = FunctionInfo(
                name=function_name,
                qualified_name=raw_name,
                signature=_render_signature(return_type, raw_name, params),
                return_type=return_type or "void",
                parameters=_parse_parameters(params),
                file_path=path,
                line_start=line_start,
                line_end=line_end,
                is_static="static" in head.split() or "STATIC" in head.split(),
                body=body,
                parser_confidence="medium",
            )

            fn.preprocessor_conditions = _active_preprocessor_conditions(
                original,
                fn.line_start,
            )
            fn.preprocessor_blocks = _preprocessor_blocks(
                original,
                fn.line_start,
                fn.line_end,
            )

            self._analyze_body(fn, body)

            try:
                fn.body_block = parse_block(body, base_line=fn.line_start)
            except Exception as exc:
                fn.assumptions.append(f"Structured body parse failed: {exc}")

            pf.functions.append(fn)
            spans.append((match.start(), body_end))
            consumed_decl_ranges.append((match.start(), body_end))
            pos = body_end

        # Extract prototypes/declarations not already covered by definitions.
        for match in _FUNC_DECL_RE.finditer(sanitized):
            if any(start <= match.start() < end for start, end in consumed_decl_ranges):
                continue

            head = match.group("head").strip()
            raw_name = re.sub(r"\s+", "", match.group("name"))
            function_name = raw_name.split("::")[-1]
            params = match.group("params").strip()

            if function_name in _CONTROL_KEYWORDS or not head:
                continue

            return_type = _normalize_return_type(head)

            if not return_type:
                continue

            if any(f.name == function_name and not f.is_declaration_only for f in pf.functions):
                continue

            pf.functions.append(
                FunctionInfo(
                    name=function_name,
                    qualified_name=raw_name,
                    signature=_render_signature(return_type, raw_name, params),
                    return_type=return_type or "void",
                    parameters=_parse_parameters(params),
                    file_path=path,
                    line_start=_line_of(sanitized, match.start()),
                    line_end=_line_of(sanitized, match.end()),
                    is_static="static" in head.split() or "STATIC" in head.split(),
                    is_declaration_only=True,
                    parser_confidence="low",
                )
            )

        return spans

    def _analyze_body(self, fn: FunctionInfo, body: str) -> None:
        local_names = {parameter.name for parameter in fn.parameters}

        # Function calls.
        for match in _CALL_RE.finditer(body):
            callee = match.group("name")

            if callee in _CONTROL_KEYWORDS or callee in local_names:
                continue

            line = _line_of(body, match.start()) + fn.line_start - 1

            fn.calls.append(
                CallInfo(
                    caller=fn.name,
                    callee=callee,
                    call_type=CallType.UNRESOLVED,
                    arguments=_split_arguments(_extract_paren_after(body, match.start())),
                    line_number=line,
                )
            )

        # Control constructs.
        for keyword in ("if", "for", "while", "switch", "do"):
            for match in re.finditer(rf"\b{keyword}\b", body):
                condition = _extract_paren_after(body, match.end())
                line = _line_of(body, match.start()) + fn.line_start - 1

                cc = ControlConstruct(
                    kind=keyword,
                    condition=condition,
                    line_number=line,
                    summary=_summarize_condition(keyword, condition),
                )

                fn.control_constructs.append(cc)

                if keyword in {"for", "while", "do"}:
                    fn.loops.append(cc)
                elif keyword == "if":
                    fn.conditions.append(cc)

        fn.return_paths = len(re.findall(r"\breturn\b", body))

        self._extract_switch_cases(fn, body)

    def _extract_switch_cases(self, fn: FunctionInfo, body: str) -> None:
        for switch_match in re.finditer(r"\bswitch\b", body):
            condition = _extract_paren_after(body, switch_match.end())
            brace = body.find("{", switch_match.end())

            if brace == -1:
                continue

            end = _match_brace(body, brace)
            block = body[brace:end]

            case_re = re.compile(
                r"\bcase\s+"
                r"(?P<label>[A-Za-z_]\w*(?:\s*::\s*[A-Za-z_]\w*)*|0[xX][0-9a-fA-F]+|\d+)"
                r"\s*:"
            )

            cases: list[SwitchCase] = []

            for case_match in case_re.finditer(block):
                cases.append(
                    SwitchCase(
                        label=case_match.group("label").strip(),
                        is_default=False,
                    )
                )

            if re.search(r"\bdefault\s*:", block):
                cases.append(
                    SwitchCase(
                        label="default",
                        is_default=True,
                    )
                )

            if cases:
                fn.switch_cases.extend(cases)

                fn.control_constructs.append(
                    ControlConstruct(
                        kind="switch",
                        condition=condition,
                        line_number=_line_of(body, switch_match.start()) + fn.line_start - 1,
                        summary=f"Switch on {condition}" if condition else "Switch",
                    )
                )

    def _extract_globals(
        self,
        text: str,
        path: str,
        pf: ParsedFile,
        function_spans: list[tuple[int, int]],
    ) -> None:
        def inside_function(idx: int) -> bool:
            return any(start <= idx < end for start, end in function_spans)

        # Top-level variable declarations ending with ";"
        global_re = re.compile(
            r"(?P<decl>[A-Za-z_][\w\s\*\&\[\]]*?)\s*(?:=\s*[^;]+)?;",
            re.MULTILINE,
        )

        for match in global_re.finditer(text):
            if inside_function(match.start()):
                continue

            decl = match.group("decl").strip()

            if not decl:
                continue

            if "(" in decl or ")" in decl:
                continue

            tokens = decl.split()

            if len(tokens) < 2:
                continue

            if tokens[0] in {"typedef", "return", "struct", "union", "enum", "else"}:
                continue

            parsed = _parse_declarator(decl)

            if not parsed or not parsed.name:
                continue

            pf.variables.append(
                VariableInfo(
                    name=parsed.name,
                    type=parsed.type,
                    is_static="static" in tokens,
                    is_const="const" in tokens,
                    file_path=path,
                    line_number=_line_of(text, match.start()),
                )
            )


def _normalize_return_type(head: str) -> str:
    tokens = [token for token in head.replace("*", " * ").split() if token]
    kept = [token for token in tokens if token not in _TYPE_QUALIFIERS]
    return " ".join(kept).replace(" *", "*").strip()


def _render_signature(return_type: str, name: str, params: str) -> str:
    return f"{return_type or 'void'} {name}({params})".strip()


def _parse_parameters(params: str) -> list[ParameterInfo]:
    params = params.strip()

    if params in {"", "void"}:
        return []

    result: list[ParameterInfo] = []
    depth = 0
    current = ""

    for ch in params:
        if ch in "<([":
            depth += 1
        elif ch in ">)]":
            depth -= 1

        if ch == "," and depth == 0:
            parsed = _parse_declarator(current.strip())

            if parsed:
                result.append(parsed)

            current = ""
        else:
            current += ch

    if current.strip():
        parsed = _parse_declarator(current.strip())

        if parsed:
            result.append(parsed)

    return result


def _parse_declarator(text: str) -> Optional[ParameterInfo]:
    """
    Parse one declarator.

    Examples:
        int value
        const Foo* ptr
        uint8_t data[10]
        MyType& ref
    """
    text = text.strip().rstrip(";")

    if not text or text == "void":
        return None

    is_const = bool(re.search(r"\bconst\b", text))
    is_pointer = "*" in text
    is_reference = "&" in text
    is_array = "[" in text and "]" in text

    # Remove array suffixes before finding the name.
    text = re.sub(r"\[[^\]]*\]", "", text)

    # Remove common qualifiers while preserving the flags above.
    for keyword in (
        "const",
        "static",
        "extern",
        "volatile",
        "register",
        "inline",
        "auto",
    ):
        text = re.sub(rf"\b{keyword}\b", " ", text)

    cleaned = re.sub(r"\s+", " ", text).strip()

    # Name is the final identifier after pointer/reference symbols are spaced.
    name_match = re.search(
        r"([A-Za-z_]\w*)\s*$",
        cleaned.replace("*", " ").replace("&", " "),
    )

    if not name_match:
        type_only = cleaned.replace("*", "").replace("&", "").strip()

        return ParameterInfo(
            name="",
            type=type_only,
            is_pointer=is_pointer,
            is_reference=is_reference,
            is_const=is_const,
            is_array=is_array,
        )

    name = name_match.group(1)
    type_part = cleaned[: name_match.start()].strip()

    if not type_part:
        type_part = cleaned.replace(name, "").strip() or "int"

    type_part = type_part.replace("&", "").strip()

    return ParameterInfo(
        name=name,
        type=type_part or "int",
        is_pointer=is_pointer,
        is_reference=is_reference,
        is_const=is_const,
        is_array=is_array,
    )


def _extract_paren_after(text: str, start: int) -> str:
    """
    Return contents of the first balanced (...) at or after start.
    """
    i = text.find("(", start)

    if i == -1:
        return ""

    depth = 0
    out: list[str] = []

    while i < len(text):
        ch = text[i]

        if ch == "(":
            depth += 1

            if depth == 1:
                i += 1
                continue

        elif ch == ")":
            depth -= 1

            if depth == 0:
                break

        out.append(ch)
        i += 1

    return "".join(out).strip()


def _split_arguments(args: str) -> list[str]:
    args = args.strip()

    if not args:
        return []

    result: list[str] = []
    current: list[str] = []
    depth = 0

    for ch in args:
        if ch in "([{<":
            depth += 1
        elif ch in ")]}>" and depth > 0:
            depth -= 1

        if ch == "," and depth == 0:
            value = "".join(current).strip()

            if value:
                result.append(value)

            current = []
        else:
            current.append(ch)

    if current:
        value = "".join(current).strip()

        if value:
            result.append(value)

    return result


def _summarize_condition(keyword: str, condition: str) -> str:
    condition = condition.strip()

    if keyword == "if":
        return f"Decision: {condition}" if condition else "Decision"

    if keyword in {"for", "while"}:
        return f"Loop while {condition}" if condition else "Loop"

    if keyword == "do":
        return f"Do-while loop while {condition}" if condition else "Do-while loop"

    if keyword == "switch":
        return f"Switch on {condition}" if condition else "Switch"

    return condition