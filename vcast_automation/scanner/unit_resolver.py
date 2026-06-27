from __future__ import annotations

from pathlib import Path
from typing import Any


def _format_pattern(pattern: str, unit: str, source_stem: str) -> str:
    return pattern.format(unit=unit, source_stem=source_stem)


def resolve_unit_context(source_path: str | Path, config: dict[str, Any]) -> dict[str, str]:
    path = Path(source_path)
    source_stem = path.stem

    defaults = config.get("defaults", {}) or {}
    units = config.get("units", {}) or {}

    unit_name_strategy = defaults.get("unit_name_strategy", "source_stem")
    unit_name = source_stem if unit_name_strategy == "source_stem" else source_stem

    unit_override = units.get(unit_name, {}) or {}
    if unit_override.get("unit_name"):
        unit_name = str(unit_override["unit_name"])
        unit_override = units.get(unit_name, unit_override) or unit_override

    env_pattern = defaults.get("environment_name_pattern", "{unit}_ENV")
    output_pattern = defaults.get("output_file_pattern", "{unit}.tst")

    environment_name = unit_override.get("environment_name") or _format_pattern(
        env_pattern, unit=unit_name, source_stem=source_stem
    )
    output_file = unit_override.get("output_file") or _format_pattern(
        output_pattern, unit=unit_name, source_stem=source_stem
    )

    return {
        "source_path": str(path),
        "source_stem": source_stem,
        "unit_name": unit_name,
        "environment_name": str(environment_name),
        "output_file": str(output_file),
    }
