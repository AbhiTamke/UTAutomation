from __future__ import annotations

from vcast_automation.models.core import TestCasePlan


def _qualified_param_name(plan: TestCasePlan, param_name: str) -> str:
    return f"{plan.unit_name}.{plan.subprogram_name}.{param_name}"


def _as_directive(prefix: str, value: str) -> str:
    value = value.strip()
    if value.startswith(prefix):
        return value
    return f"{prefix}{value}"


def render_values(plan: TestCasePlan) -> str:
    """
    Render VectorCAST stubs and values.

    Order intentionally matches common manual style:
    1. TEST.STUB
    2. advanced/raw TEST.VALUE lines
    3. normal qualified parameter TEST.VALUE lines
    4. expected values
    """
    lines: list[str] = []

    for stub in plan.stub_lines:
        if stub.strip():
            lines.append(_as_directive("TEST.STUB:", stub))

    for raw in plan.raw_value_lines:
        if raw.strip():
            lines.append(_as_directive("TEST.VALUE:", raw))

    for param_name, value in sorted(plan.input_values.items()):
        if param_name and value is not None:
            lines.append(f"TEST.VALUE:{_qualified_param_name(plan, param_name)}:{value}")

    for raw_expected in plan.raw_expected_lines:
        if raw_expected.strip():
            lines.append(_as_directive("TEST.EXPECTED:", raw_expected))

    for expected_name, expected_value in sorted(plan.expected_values.items()):
        if expected_name and expected_value is not None:
            lines.append(f"TEST.EXPECTED:{expected_name}:{expected_value}")

    return "\n".join(lines)