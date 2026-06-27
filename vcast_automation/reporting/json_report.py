from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from vcast_automation.models.core import dataclass_to_dict


def write_json_report(path: str | Path, payload: dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        json.dumps(dataclass_to_dict(payload), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )