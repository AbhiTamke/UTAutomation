from __future__ import annotations

import re
from typing import Optional

from vcast_automation.parser_engine.code_model import Statement, StmtKind, SwitchCase


_KEYWORDS = {
    "if", "for", "while", "switch", "return", "sizeof", "defined", "do", "else",
    "case", "default", "break", "continue", "goto", "static_cast",
    "reinterpret_cast", "const_cast", "dynamic_cast", "typedef", "struct",
    "union", "enum",
}

_CALL_RE = re.compile(r"\b([A-Za-z_]\w*)\s*\(")
_IDENT_RE = re.compile(r"[A-Za-z_]\w*")
_ASSIGN_RE = re.compile(
    r"^\s*(?P<lhs>[A-Za-z_]\w*(?:\s*(?:\[[^\]]*\]|\.\s*\w+|->\s*\w+))*)\s*"
    r"(?:[-+*/|&%]|<<|>>)?=(?!=)"
)


def _sanitize(text: str) -> str:
    out: list[str] = []
    i = 0
    state = "code"

    while i < len(text):
        ch = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ""

        if state == "code":
            if ch == "/" and nxt == "/":
                state = "line"
                out.append("  ")
                i += 2
                continue
            if ch == "/" and nxt == "*":
                state = "block"
                out.append("  ")
                i += 2
                continue
            if ch == '"':
                state = "str"
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

        if state == "line":
            if ch == "\n":
                state = "code"
                out.append("\n")
            else:
                out.append(" ")
            i += 1
            continue

        if state == "block":
            if ch == "*" and nxt == "/":
                state = "code"
                out.append("  ")
                i += 2
                continue
            out.append("\n" if ch == "\n" else " ")
            i += 1
            continue

        if state in {"str", "char"}:
            if ch == "\\":
                out.append("  ")
                i += 2
                continue
            if state == "str" and ch == '"':
                state = "code"
            elif state == "char" and ch == "'":
                state = "code"
            out.append("\n" if ch == "\n" else " ")
            i += 1
            continue

    return "".join(out)


def _match_paren(text: str, open_idx: int) -> int:
    depth = 0
    for i in range(open_idx, len(text)):
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
            if depth == 0:
                return i
    return len(text) - 1


def _match_brace(text: str, open_idx: int) -> int:
    depth = 0
    for i in range(open_idx, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i
    return len(text) - 1


def _extract_calls(text: str) -> list[str]:
    calls: list[str] = []
    for match in _CALL_RE.finditer(text):
        name = match.group(1)
        if name not in _KEYWORDS and name not in calls:
            calls.append(name)
    return calls


def _extract_assigned(text: str) -> list[str]:
    match = _ASSIGN_RE.match(text)
    if not match:
        return []
    lhs = match.group("lhs")
    ident = _IDENT_RE.match(lhs.strip())
    return [ident.group(0)] if ident else []


def parse_block(body_text: str, base_line: int = 0, _depth: int = 0) -> list[Statement]:
    text = _sanitize(body_text)

    # Remove outer braces if body text includes them.
    stripped = text.strip()
    if stripped.startswith("{") and stripped.endswith("}"):
        first = text.find("{")
        last = text.rfind("}")
        text = text[first + 1:last]

    return _parse_statements(text, base_line, _depth)


def _parse_statements(text: str, base_line: int, depth: int) -> list[Statement]:
    statements: list[Statement] = []
    i = 0

    while i < len(text):
        while i < len(text) and text[i].isspace():
            i += 1

        if i >= len(text):
            break

        if text.startswith("if", i) and _keyword_boundary(text, i, "if"):
            stmt, i = _parse_if(text, i, base_line, depth)
            statements.append(stmt)
            continue

        if text.startswith("for", i) and _keyword_boundary(text, i, "for"):
            stmt, i = _parse_loop(text, i, "for", base_line, depth)
            statements.append(stmt)
            continue

        if text.startswith("while", i) and _keyword_boundary(text, i, "while"):
            stmt, i = _parse_loop(text, i, "while", base_line, depth)
            statements.append(stmt)
            continue

        if text.startswith("do", i) and _keyword_boundary(text, i, "do"):
            stmt, i = _parse_do(text, i, base_line, depth)
            statements.append(stmt)
            continue

        if text.startswith("switch", i) and _keyword_boundary(text, i, "switch"):
            stmt, i = _parse_switch(text, i, base_line, depth)
            statements.append(stmt)
            continue

        if text.startswith("return", i) and _keyword_boundary(text, i, "return"):
            stmt, i = _parse_return(text, i, base_line)
            statements.append(stmt)
            continue

        stmt, i = _parse_simple(text, i, base_line)
        if stmt:
            statements.append(stmt)

    return statements


def _keyword_boundary(text: str, i: int, keyword: str) -> bool:
    before = text[i - 1] if i > 0 else " "
    after_pos = i + len(keyword)
    after = text[after_pos] if after_pos < len(text) else " "
    return not (before.isalnum() or before == "_") and not (after.isalnum() or after == "_")


def _read_clause_body(text: str, i: int, base_line: int, depth: int) -> tuple[list[Statement], int]:
    while i < len(text) and text[i].isspace():
        i += 1

    if i < len(text) and text[i] == "{":
        close = _match_brace(text, i)
        inner = text[i + 1:close]
        body = _parse_statements(inner, base_line + text.count("\n", 0, i), depth + 1)
        return body, close + 1

    stmt, next_i = _parse_statement_single(text, i, base_line, depth)
    return ([stmt] if stmt else []), next_i


def _parse_statement_single(
    text: str,
    i: int,
    base_line: int,
    depth: int,
) -> tuple[Optional[Statement], int]:
    if text.startswith("if", i) and _keyword_boundary(text, i, "if"):
        stmt, j = _parse_if(text, i, base_line, depth)
        return stmt, j
    if text.startswith("for", i) and _keyword_boundary(text, i, "for"):
        stmt, j = _parse_loop(text, i, "for", base_line, depth)
        return stmt, j
    if text.startswith("while", i) and _keyword_boundary(text, i, "while"):
        stmt, j = _parse_loop(text, i, "while", base_line, depth)
        return stmt, j
    if text.startswith("return", i) and _keyword_boundary(text, i, "return"):
        stmt, j = _parse_return(text, i, base_line)
        return stmt, j
    return _parse_simple(text, i, base_line)


def _parse_if(text: str, i: int, base_line: int, depth: int) -> tuple[Statement, int]:
    paren_open = text.find("(", i)
    if paren_open == -1:
        return Statement(kind=StmtKind.SIMPLE, line=base_line + text.count("\n", 0, i)), len(text)

    paren_close = _match_paren(text, paren_open)
    condition = text[paren_open + 1:paren_close].strip()
    then_body, j = _read_clause_body(text, paren_close + 1, base_line, depth)

    else_body: list[Statement] = []
    k = j
    while k < len(text) and text[k].isspace():
        k += 1

    if text.startswith("else", k) and _keyword_boundary(text, k, "else"):
        else_body, j = _read_clause_body(text, k + 4, base_line, depth)

    stmt = Statement(
        kind=StmtKind.IF,
        line=base_line + text.count("\n", 0, i),
        condition=condition,
        body=then_body,
        else_body=else_body,
    )
    return stmt, j


def _parse_loop(text: str, i: int, kw: str, base_line: int, depth: int) -> tuple[Statement, int]:
    paren_open = text.find("(", i)
    paren_close = _match_paren(text, paren_open)
    condition = text[paren_open + 1:paren_close].strip()
    body, j = _read_clause_body(text, paren_close + 1, base_line, depth)

    stmt = Statement(
        kind=StmtKind.LOOP,
        line=base_line + text.count("\n", 0, i),
        loop_kind=kw,
        condition=condition,
        body=body,
    )
    return stmt, j


def _parse_do(text: str, i: int, base_line: int, depth: int) -> tuple[Statement, int]:
    body, j = _read_clause_body(text, i + 2, base_line, depth)
    k = j

    while k < len(text) and text[k].isspace():
        k += 1

    condition = ""
    if text.startswith("while", k):
        paren_open = text.find("(", k)
        paren_close = _match_paren(text, paren_open)
        condition = text[paren_open + 1:paren_close].strip()
        semi = text.find(";", paren_close)
        j = len(text) if semi == -1 else semi + 1

    stmt = Statement(
        kind=StmtKind.LOOP,
        line=base_line + text.count("\n", 0, i),
        loop_kind="do",
        condition=condition,
        body=body,
    )
    return stmt, j


def _parse_switch(text: str, i: int, base_line: int, depth: int) -> tuple[Statement, int]:
    paren_open = text.find("(", i)
    paren_close = _match_paren(text, paren_open)
    condition = text[paren_open + 1:paren_close].strip()

    brace_open = text.find("{", paren_close)
    if brace_open == -1:
        return Statement(
            kind=StmtKind.SWITCH,
            line=base_line + text.count("\n", 0, i),
            condition=condition,
        ), len(text)

    brace_close = _match_brace(text, brace_open)
    block = text[brace_open + 1:brace_close]

    cases: list[SwitchCase] = []
    case_re = re.compile(
        r"\bcase\s+(?P<label>[A-Za-z_]\w*(?:\s*::\s*[A-Za-z_]\w*)*|0[xX][0-9a-fA-F]+|\d+)\s*:"
    )

    for match in case_re.finditer(block):
        cases.append(SwitchCase(label=match.group("label").strip()))

    if re.search(r"\bdefault\s*:", block):
        cases.append(SwitchCase(label="default", is_default=True))

    stmt = Statement(
        kind=StmtKind.SWITCH,
        line=base_line + text.count("\n", 0, i),
        condition=condition,
        cases=cases,
    )
    return stmt, brace_close + 1


def _parse_return(text: str, i: int, base_line: int) -> tuple[Statement, int]:
    end = text.find(";", i)
    end = len(text) if end == -1 else end
    value = text[i + len("return"):end].strip()

    stmt = Statement(
        kind=StmtKind.RETURN,
        line=base_line + text.count("\n", 0, i),
        return_value=value,
    )
    return stmt, end + 1


def _parse_simple(text: str, i: int, base_line: int) -> tuple[Optional[Statement], int]:
    depth_p = depth_b = depth_c = 0
    j = i

    while j < len(text):
        ch = text[j]
        if ch == "(":
            depth_p += 1
        elif ch == ")":
            depth_p -= 1
        elif ch == "[":
            depth_b += 1
        elif ch == "]":
            depth_b -= 1
        elif ch == "{":
            depth_c += 1
        elif ch == "}":
            depth_c -= 1
            if depth_c < 0:
                break
        elif ch == ";" and depth_p <= 0 and depth_b <= 0 and depth_c <= 0:
            break
        j += 1

    fragment = text[i:j].strip()
    next_i = j + 1

    if not fragment:
        return None, next_i

    calls = _extract_calls(fragment)
    assigned = _extract_assigned(fragment)
    kind = StmtKind.CALL if calls and not assigned else StmtKind.SIMPLE

    stmt = Statement(
        kind=kind,
        line=base_line + text.count("\n", 0, i),
        text=fragment[:120],
        calls=calls,
        assigned=assigned,
    )
    return stmt, next_i