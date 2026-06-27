from __future__ import annotations

from pathlib import Path

from vcast_automation.models.core import TraceabilityRecord


class EapxGuidProvider:
    """
    vcast_automation wrapper around the EA GUID extractor.

    Supports repository paths handled by eapx_guid_extractor:
    - .eapx/.eap via Access/pyodbc or COM fallback
    - .qea/.qeax via SQLite

    Behavior:
    - If no repository path is configured, provider returns missing.
    - If lookup has exactly one strict match, returns matched.
    - If lookup fails or dependencies are unavailable, returns missing with source info.
    - Never fabricates GUIDs.
    """

    def __init__(self, repository_path: str | Path | None, *, backend: str = "auto"):
        self.repository_path = Path(repository_path) if repository_path else None
        self.backend = backend or "auto"
        self.available = bool(self.repository_path and self.repository_path.exists())
        self.last_error: str = ""

    def find_guid(
        self,
        unit_name: str,
        function_name: str,
        source_path: str | None = None,
        class_name: str | None = None,
    ) -> TraceabilityRecord:
        if not self.available or self.repository_path is None:
            return TraceabilityRecord(
                unit=unit_name,
                function=function_name,
                guid="",
                source="eapx_guid_provider",
                match_status="missing",
                match_confidence="none",
            )

        try:
            from vcast_automation.traceability.eapx_guid_extractor import EapxGuidExtractor
        except Exception as exc:
            self.last_error = str(exc)
            return TraceabilityRecord(
                unit=unit_name,
                function=function_name,
                guid="",
                source=f"eapx_guid_provider:import_error:{self.last_error}",
                match_status="missing",
                match_confidence="none",
            )

        try:
            with EapxGuidExtractor(self.repository_path, backend=self.backend) as extractor:
                matches = extractor.extract_guid_matches(
                    function_name,
                    owner=class_name,
                )
        except Exception as exc:
            self.last_error = str(exc)
            return TraceabilityRecord(
                unit=unit_name,
                function=function_name,
                guid="",
                source=f"eapx_guid_provider:lookup_error:{self.last_error}",
                match_status="missing",
                match_confidence="none",
            )

        if len(matches) == 1:
            return TraceabilityRecord(
                unit=unit_name,
                function=function_name,
                guid=matches[0].guid,
                source=f"eapx:{self.repository_path.name}:{matches[0].object_type}",
                match_status="matched",
                match_confidence=matches[0].confidence,
            )

        if len(matches) > 1:
            return TraceabilityRecord(
                unit=unit_name,
                function=function_name,
                guid="",
                source=f"eapx:{self.repository_path.name}:ambiguous",
                match_status="ambiguous",
                match_confidence="none",
            )

        return TraceabilityRecord(
            unit=unit_name,
            function=function_name,
            guid="",
            source=f"eapx:{self.repository_path.name}:missing",
            match_status="missing",
            match_confidence="none",
        )
