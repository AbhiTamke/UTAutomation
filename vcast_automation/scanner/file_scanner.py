from __future__ import annotations

import fnmatch
from pathlib import Path


def scan_source_files(config: dict) -> list[Path]:
    input_cfg = config.get("input", {})

    raw_source_roots = input_cfg.get("source_roots", [])
    raw_source_files = input_cfg.get("source_files", [])
    raw_include_extensions = input_cfg.get("include_extensions", [".c", ".cpp", ".h", ".hpp"])
    raw_exclude_dirs = input_cfg.get("exclude_dirs", [])
    raw_exclude_files = input_cfg.get("exclude_files", [])

    source_roots = [Path(p) for p in raw_source_roots if isinstance(p, str) and p.strip()]
    source_files = [Path(p) for p in raw_source_files if isinstance(p, str) and p.strip()]
    include_extensions = {
        ext.lower() for ext in raw_include_extensions if isinstance(ext, str) and ext.strip()
    }
    exclude_dirs = {name for name in raw_exclude_dirs if isinstance(name, str) and name.strip()}
    exclude_files = [pattern for pattern in raw_exclude_files if isinstance(pattern, str) and pattern.strip()]

    results: list[Path] = []

    for file_path in source_files:
        if file_path.exists() and file_path.suffix.lower() in include_extensions:
            results.append(file_path)

    for root in source_roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if any(part in exclude_dirs for part in path.parts):
                continue
            if path.suffix.lower() not in include_extensions:
                continue
            if any(fnmatch.fnmatch(path.name, pattern) for pattern in exclude_files):
                continue
            results.append(path)

    return sorted(set(results))