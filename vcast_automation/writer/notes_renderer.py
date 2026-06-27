from __future__ import annotations

from vcast_automation.models.core import TestCasePlan


DEFAULT_COVERAGE_ASIL = [
    "Statement Coverage",
    "Branch Coverage",
    "MC/DC Coverage",
    "control flow verification",
    "visual inspection",
]


def _format_asil_lines(items: list[str]) -> list[str]:
    if not items:
        items = DEFAULT_COVERAGE_ASIL

    rendered: list[str] = []
    for item in items:
        text = str(item).strip()
        if not text:
            continue
        rendered.append(text if text.startswith("- ") else f"- {text}")
    return rendered


def render_notes(plan: TestCasePlan) -> str:
    """
    Render a VectorCAST TEST.NOTES block.

    This matches the manual style more closely by including:
    - ID
    - Description
    - ReviewID
    - Status
    - Notes
    - GUID
    - ASIL/coverage bullets
    - Priority
    """
    guid_value = "" if plan.guid in {None, ""} else plan.guid
    review_value = "TBD" if plan.review_id in {None, ""} else plan.review_id

    lines = [
        "TEST.NOTES:",
        "##ID##",
        plan.test_case_id,
        "##End.ID##",
        "##Description##",
        plan.description,
        "##End.Description##",
        "##ReviewID##",
        review_value,
        "##End.ReviewID##",
        "##Status##",
        plan.status or "Draft",
        "##End.Status##",
        "##Notes##",
    ]

    if plan.notes:
        lines.append(plan.notes)

    lines.extend(
        [
            "##End.Notes##",
            "##GUID##",
            guid_value,
            "##End.GUID##",
            "##ASIL##",
        ]
    )

    lines.extend(_format_asil_lines(plan.asil))

    lines.extend(
        [
            "##End.ASIL##",
            "##Priority##",
            plan.priority or "High",
            "##End.Priority##",
            "TEST.END_NOTES:",
        ]
    )

    return "\n".join(lines)