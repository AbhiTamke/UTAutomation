from __future__ import annotations

from pathlib import Path

from vcast_automation.diagnostics.codes import (
    TST_DUPLICATE_TEST_NAME,
    TST_MISSING_NOTES_MARKER,
    TST_UNBALANCED_TEST_BLOCK,
    TST_UNRESOLVED_GUID_TBD,
    TST_UNRESOLVED_REVIEWID_TBD,
)
from vcast_automation.models.core import Diagnostic


REQUIRED_MARKERS = [
    "TEST.NOTES:",
    "##ID##",
    "##End.ID##",
    "##Description##",
    "##End.Description##",
    "##ReviewID##",
    "##End.ReviewID##",
    "##Status##",
    "##End.Status##",
    "##Notes##",
    "##End.Notes##",
    "##GUID##",
    "##End.GUID##",
    "##ASIL##",
    "##End.ASIL##",
    "TEST.END_NOTES:",
]

OPTIONAL_REFERENCE_MARKERS = [
    "##Priority##",
    "##End.Priority##",
]


def _strip_escape(line: str) -> str:
    return line.strip().lstrip("\\").strip()


def validate_tst(path: str | Path) -> list[Diagnostic]:
    p = Path(path)
    text = p.read_text(encoding="utf-8", errors="replace")
    normalized_lines = [_strip_escape(line) for line in text.splitlines()]
    normalized_text = "\n".join(normalized_lines)
    diagnostics: list[Diagnostic] = []

    if normalized_lines.count("TEST.NEW") != normalized_lines.count("TEST.END"):
        diagnostics.append(
            Diagnostic(
                code=TST_UNBALANCED_TEST_BLOCK,
                message="TEST.NEW and TEST.END count mismatch.",
                severity="error",
                source=str(p),
            )
        )

    for marker in REQUIRED_MARKERS:
        if marker not in normalized_text:
            diagnostics.append(
                Diagnostic(
                    code=TST_MISSING_NOTES_MARKER,
                    message=f"Missing required notes marker: {marker}",
                    severity="error",
                    source=str(p),
                )
            )

    for marker in OPTIONAL_REFERENCE_MARKERS:
        if marker not in normalized_text:
            diagnostics.append(
                Diagnostic(
                    code=TST_MISSING_NOTES_MARKER,
                    message=f"Missing reference-style optional notes marker: {marker}",
                    severity="warning",
                    source=str(p),
                )
            )

    names: list[str] = []
    for line in normalized_lines:
        if line.startswith("TEST.NAME:"):
            names.append(line.split(":", 1)[1].strip())

    duplicate_names = sorted({name for name in names if names.count(name) > 1})
    for name in duplicate_names:
        diagnostics.append(
            Diagnostic(
                code=TST_DUPLICATE_TEST_NAME,
                message=f"Duplicate TEST.NAME found: {name}",
                severity="error",
                source=str(p),
            )
        )

    if "##ReviewID##\nTBD\n##End.ReviewID##" in normalized_text:
        diagnostics.append(
            Diagnostic(
                code=TST_UNRESOLVED_REVIEWID_TBD,
                message="Unresolved ReviewID marked as TBD.",
                severity="warning",
                source=str(p),
            )
        )

    if "##GUID##\nTBD\n##End.GUID##" in normalized_text:
        diagnostics.append(
            Diagnostic(
                code=TST_UNRESOLVED_GUID_TBD,
                message="Unresolved GUID marked as TBD.",
                severity="warning",
                source=str(p),
            )
        )

    return diagnostics