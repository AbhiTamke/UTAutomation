from __future__ import annotations

import json
from pathlib import Path

from vcast_automation.models.core import TraceabilityRecord


class GuidProvider:
    def find_guid(
        self,
        unit_name: str,
        function_name: str,
        source_path: str | None = None,
        class_name: str | None = None,
    ) -> TraceabilityRecord:
        return TraceabilityRecord(
            unit=unit_name,
            function=function_name,
            guid="",
            match_status="missing",
            match_confidence="none",
        )


class JsonGuidProvider(GuidProvider):
    def __init__(self, json_path: str | Path | None):
        self.records: list[dict] = []
        if json_path:
            path = Path(json_path)
            if path.exists():
                data = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    self.records = data

    def find_guid(
        self,
        unit_name: str,
        function_name: str,
        source_path: str | None = None,
        class_name: str | None = None,
    ) -> TraceabilityRecord:
        matches = []

        for row in self.records:
            row_unit = str(row.get("unit", "")).strip()
            row_function = str(row.get("function", "")).strip()
            row_source = str(row.get("source_path", "")).strip()

            if row_unit == unit_name and row_function == function_name:
                if source_path and row_source and Path(row_source).name != Path(source_path).name:
                    continue
                matches.append(row)

        if len(matches) == 1:
            return TraceabilityRecord(
                unit=unit_name,
                function=function_name,
                guid=str(matches[0].get("guid", "")),
                source="json_guid_provider",
                match_status="matched",
                match_confidence="high",
            )

        if len(matches) > 1:
            return TraceabilityRecord(
                unit=unit_name,
                function=function_name,
                guid="",
                source="json_guid_provider",
                match_status="ambiguous",
                match_confidence="none",
            )

        return TraceabilityRecord(
            unit=unit_name,
            function=function_name,
            guid="",
            source="json_guid_provider",
            match_status="missing",
            match_confidence="none",
        )


def inspect_eapx(path: str | Path) -> dict:
    """
    Safe placeholder inspector.

    Real .eapx database access is intentionally not hard-coded until a real
    project sample confirms whether the file is Access-like, SQLite-like, or
    another storage format.
    """
    p = Path(path)
    if not p.exists():
        return {
            "path": str(p),
            "exists": False,
            "status": "missing",
        }

    header = p.read_bytes()[:32]
    return {
        "path": str(p),
        "exists": True,
        "size_bytes": p.stat().st_size,
        "header_hex": header.hex(),
        "status": "schema_unknown",
        "message": "Real .eapx GUID extraction requires schema validation with an actual sample.",
    }