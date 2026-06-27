from __future__ import annotations

import json
from pathlib import Path

from vcast_automation.models.core import TestCasePlan


class StaticTraceabilityProvider:
    """
    Optional JSON-driven traceability provider.

    JSON shape:
    [
      {
        "unit": "App_SLI",
        "function": "SLI_Init",
        "review_id": "40777978",
        "guid": "{363963D8-BE2F-4440-B9FE-B7614B07E73F}",
        "status": "In Review",
        "priority": "High"
      }
    ]
    """

    def __init__(self, path: str | Path | None):
        self.records: list[dict] = []
        if not path:
            return
        p = Path(path)
        if not p.exists():
            return
        data = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(data, list):
            self.records = data

    def apply(self, plan: TestCasePlan) -> None:
        matches = []
        for row in self.records:
            if row.get("unit") != plan.unit_name:
                continue
            if row.get("test_case_id") and row.get("test_case_id") == plan.test_case_id:
                matches.append(row)
                continue
            if row.get("function") and row.get("function") == plan.function_name:
                matches.append(row)

        if len(matches) != 1:
            return

        row = matches[0]
        if row.get("review_id"):
            plan.review_id = str(row["review_id"])
        if row.get("guid"):
            plan.guid = str(row["guid"])
        if row.get("status"):
            plan.status = str(row["status"])
        if row.get("priority"):
            plan.priority = str(row["priority"])