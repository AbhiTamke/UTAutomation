from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from vcast_automation.config.loader import load_config
from vcast_automation.parser_adapter.lightweight_adapter import LightweightParserAdapter
from vcast_automation.planner.planner import TestPlanner
from vcast_automation.reporting.json_report import write_json_report
from vcast_automation.scanner.file_scanner import scan_source_files
from vcast_automation.scanner.unit_resolver import resolve_unit_context
from vcast_automation.traceability.eapx_guid_provider import EapxGuidProvider
from vcast_automation.traceability.guid_provider import JsonGuidProvider
from vcast_automation.traceability.reviewid_xlsm_loader import ReviewIdXlsmLoader
from vcast_automation.validator.tst_validator import validate_tst
from vcast_automation.writer.tst_writer import TstWriter


SUPPORTED_SOURCE_EXTENSIONS = {
    ".c",
    ".h",
    ".cpp",
    ".hpp",
    ".cc",
    ".cxx",
    ".hh",
    ".hxx",
}


def _validate_source_arg(source_path: str) -> None:
    source = Path(source_path)
    if not source.exists():
        raise FileNotFoundError(f"Source path does not exist: {source}")
    if source.is_file() and source.suffix.lower() not in SUPPORTED_SOURCE_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_SOURCE_EXTENSIONS))
        raise ValueError(f"Unsupported source extension: {source.suffix}. Supported: {supported}")


def _normalize_config_for_cli(
    config: dict[str, Any],
    source_path: str,
    output_path: str,
    reviewid_path: str | None,
    eapx_path: str | None,
    eapx_backend: str,
    guid_map_path: str | None,
) -> dict[str, Any]:
    source = Path(source_path)

    config.setdefault("input", {})
    config.setdefault("generation", {})
    config.setdefault("traceability", {})
    config.setdefault("vectorcast", {})
    config.setdefault("validation", {})
    config.setdefault("defaults", {})
    config.setdefault("units", {})

    if source.is_file():
        config["input"]["source_roots"] = []
        config["input"]["source_files"] = [str(source)]
    else:
        config["input"]["source_roots"] = [str(source)]
        config["input"]["source_files"] = []

    config["input"].setdefault(
        "include_extensions",
        [".c", ".h", ".cpp", ".hpp", ".cc", ".cxx", ".hh", ".hxx"],
    )
    config["input"].setdefault(
        "exclude_dirs",
        ["build", "generated", "vendor", "third_party", ".git", "out"],
    )
    config["input"].setdefault("exclude_files", ["*_pb.c", "*_generated.c"])

    config["generation"]["output_dir"] = output_path

    if reviewid_path:
        config["traceability"]["reviewid_xlsm_path"] = reviewid_path
    if guid_map_path:
        config["traceability"]["guid_mapping_json"] = guid_map_path
    if eapx_path:
        config["traceability"]["ea_eapx_path"] = eapx_path
        config["traceability"]["ea_eapx_backend"] = eapx_backend

    metadata = config.get("metadata", {}) or {}
    if "default_status" in metadata:
        config["generation"]["default_status"] = metadata["default_status"]
    if "default_priority" in metadata:
        config["generation"]["default_priority"] = metadata["default_priority"]
    if "default_asil" in metadata:
        config["generation"]["default_asil"] = metadata["default_asil"]

    rules = config.get("rules", {}) or {}
    if "enable_project_rules" in rules:
        config["generation"]["enable_project_rules"] = rules["enable_project_rules"]
    if "enable_expected_from_mapping" in rules:
        config["generation"]["enable_rich_expected"] = rules["enable_expected_from_mapping"]

    return config


def _apply_unit_context_to_source_model(source_model, config: dict[str, Any]):
    context = resolve_unit_context(source_model.source_path, config)
    source_model.unit_name = context["unit_name"]
    source_model.source_stem = Path(source_model.source_path).stem
    for fn in source_model.functions:
        fn.unit_name = context["unit_name"]
    return source_model, context


def _enrich_plans(config: dict[str, Any], plans) -> None:
    trace_cfg = config.get("traceability", {}) or {}
    review_loader = ReviewIdXlsmLoader(trace_cfg.get("reviewid_xlsm_path"))
    json_guid_provider = JsonGuidProvider(trace_cfg.get("guid_mapping_json"))
    eapx_guid_provider = EapxGuidProvider(
        trace_cfg.get("ea_eapx_path"),
        backend=trace_cfg.get("ea_eapx_backend", "auto"),
    )

    missing_review = trace_cfg.get("missing_review_id", "TBD")
    missing_guid = trace_cfg.get("missing_guid", "TBD")

    for plan in plans:
        review = review_loader.find(
            test_case_id=plan.test_case_id,
            unit=plan.unit_name,
            function=plan.function_name,
            subprogram=plan.subprogram_name,
        )
        if review.match_status == "matched":
            plan.review_id = review.review_id or missing_review
            if review.requirement_key:
                plan.requirement_keys.append(review.requirement_key)
            if review.status:
                plan.status = review.status
            if review.asil:
                plan.asil = [x.strip() for x in review.asil.split(",") if x.strip()]
            if review.notes:
                plan.notes = review.notes
            if review.description:
                plan.description = review.description
        elif not getattr(plan, "review_id", "") or plan.review_id == "TBD":
            plan.review_id = missing_review

        guid = json_guid_provider.find_guid(
            unit_name=plan.unit_name,
            function_name=plan.function_name,
            source_path=plan.source_path,
        )
        if guid.match_status != "matched":
            guid = eapx_guid_provider.find_guid(
                unit_name=plan.unit_name,
                function_name=plan.function_name,
                source_path=plan.source_path,
            )

        if guid.match_status == "matched":
            plan.guid = guid.guid or missing_guid
        elif not getattr(plan, "guid", "") or plan.guid == "TBD":
            plan.guid = missing_guid


def run_automation(args: argparse.Namespace) -> int:
    _validate_source_arg(args.source)

    config = load_config(args.config)
    config = _normalize_config_for_cli(
        config=config,
        source_path=args.source,
        output_path=args.output,
        reviewid_path=args.reviewid,
        eapx_path=args.eapx,
        eapx_backend=args.eapx_backend,
        guid_map_path=args.guid_map,
    )

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    parser = LightweightParserAdapter()
    planner = TestPlanner(config)
    writer = TstWriter(config)

    source_files = scan_source_files(config)
    if not source_files:
        print("No supported source files found.")
        return 2

    generated_docs = []
    validation_results = []
    parsed_sources = []

    for source_file in source_files:
        source_model = parser.parse_file(source_file)
        source_model, unit_context = _apply_unit_context_to_source_model(source_model, config)
        parsed_sources.append(source_model)

        plans = planner.plan_source(source_model)
        _enrich_plans(config, plans)

        doc = writer.write_source(
            source_path=source_model.source_path,
            unit_name=source_model.unit_name,
            plans=plans,
            unit_context=unit_context,
        )
        generated_docs.append(doc)

        if args.validate:
            diagnostics = validate_tst(doc.output_path)
            validation_results.append({"path": doc.output_path, "diagnostics": diagnostics})

    write_json_report(
        output_dir / "utautomation_report.json",
        {
            "summary": {
                "source_files": len(source_files),
                "generated_tst_files": len(generated_docs),
                "validation_enabled": bool(args.validate),
                "eapx_enabled": bool(config.get("traceability", {}).get("ea_eapx_path")),
            },
            "sources": parsed_sources,
            "generated": generated_docs,
            "validation": validation_results,
        },
    )

    print(f"Processed source file(s): {len(source_files)}")
    print(f"Generated .tst file(s): {len(generated_docs)}")
    print(f"Output: {output_dir}")
    print(f"Report: {output_dir / 'utautomation_report.json'}")

    if args.validate:
        error_count = 0
        for result in validation_results:
            for diagnostic in result.get("diagnostics", []):
                if getattr(diagnostic, "severity", "") == "error":
                    error_count += 1
        if error_count:
            print(f"Validation completed with {error_count} error(s).")
            return 1
        print("Validation completed without errors.")

    return 0


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="UTAutomation.py",
        description="Offline VectorCAST .tst generation and traceability enrichment tool.",
    )
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("-f", "--file", dest="source", help="Source file path")
    source_group.add_argument("-F", "--folder", dest="source", help="Source folder path")

    parser.add_argument("-o", "--output", required=True, help="Output folder")
    parser.add_argument("-c", "--config", required=True, help="YAML config file")
    parser.add_argument("--validate", "-validate", action="store_true", help="Validate generated .tst files")
    parser.add_argument("--reviewid", "--review-id", dest="reviewid", default=None, help="ReviewID .xlsm/.xlsx path")
    parser.add_argument("--eapx", default=None, help="EA repository path: .eapx/.eap/.qea/.qeax")
    parser.add_argument(
        "--eapx-backend",
        choices=["auto", "access", "sqlite", "com"],
        default="auto",
        help="EA repository backend",
    )
    parser.add_argument("--guid-map", default=None, help="Optional JSON GUID mapping file")
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()
    try:
        return run_automation(args)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
