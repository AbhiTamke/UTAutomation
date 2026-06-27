from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from vcast_automation.config.loader import load_config, write_default_config
from vcast_automation.models.core import dataclass_to_dict
from vcast_automation.parser_adapter.lightweight_adapter import LightweightParserAdapter
from vcast_automation.planner.planner import TestPlanner
from vcast_automation.reporting.json_report import write_json_report
from vcast_automation.scanner.file_scanner import scan_source_files
from vcast_automation.traceability.guid_provider import JsonGuidProvider, inspect_eapx
from vcast_automation.traceability.reviewid_xlsm_loader import ReviewIdXlsmLoader
from vcast_automation.validator.tst_validator import validate_tst
from vcast_automation.writer.tst_writer import TstWriter


def cmd_init_config(args: argparse.Namespace) -> int:
    write_default_config(args.output)
    print(f"Created default config: {args.output}")
    return 0


def cmd_parse(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    parser = LightweightParserAdapter()
    files = scan_source_files(config)
    sources = [parser.parse_file(path) for path in files]

    output_dir = Path(config.get("generation", {}).get("output_dir", "./vcast_output"))
    write_json_report(output_dir / "parse_report.json", {"sources": sources})

    print(f"Parsed {len(sources)} source file(s).")
    print(f"Report: {output_dir / 'parse_report.json'}")
    return 0


def _enrich_plans(config: dict, plans):
    review_loader = ReviewIdXlsmLoader(config.get("traceability", {}).get("reviewid_xlsm_path"))
    guid_provider = JsonGuidProvider(config.get("traceability", {}).get("guid_mapping_json"))

    missing_review = config.get("traceability", {}).get("missing_review_id", "TBD")
    missing_guid = config.get("traceability", {}).get("missing_guid", "TBD")

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
                plan.asil = [item.strip() for item in review.asil.split(",") if item.strip()]
            if review.notes:
                plan.notes = review.notes
            if review.description:
                plan.description = review.description
        elif plan.review_id in {None, "", "TBD"}:
            plan.review_id = missing_review

        guid = guid_provider.find_guid(
            unit_name=plan.unit_name,
            function_name=plan.function_name,
            source_path=plan.source_path,
        )
        if guid.match_status == "matched":
            plan.guid = guid.guid or missing_guid
        elif plan.guid in {None, "", "TBD"}:
            plan.guid = missing_guid


def cmd_generate(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    parser = LightweightParserAdapter()
    planner = TestPlanner(config)
    writer = TstWriter(config)

    files = scan_source_files(config)
    generated_docs = []
    validation_results = []

    for file_path in files:
        source = parser.parse_file(file_path)
        plans = planner.plan_source(source)
        _enrich_plans(config, plans)

        if args.dry_run:
            generated_docs.append(
                {
                    "source": source,
                    "planned_tests": plans,
                    "dry_run": True,
                }
            )
            continue

        doc = writer.write_source(source.source_path, source.unit_name, plans)
        generated_docs.append(doc)

        diagnostics = validate_tst(doc.output_path)
        validation_results.append(
            {
                "path": doc.output_path,
                "diagnostics": diagnostics,
            }
        )

    output_dir = Path(config.get("generation", {}).get("output_dir", "./vcast_output"))
    write_json_report(
        output_dir / "generation_report.json",
        {
            "generated": generated_docs,
            "validation": validation_results,
            "summary": {
                "files_seen": len(files),
                "documents": len(generated_docs),
            },
        },
    )

    print(f"Processed {len(files)} source file(s).")
    print(f"Report: {output_dir / 'generation_report.json'}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    root = Path(args.path)
    files = [root] if root.is_file() else sorted(root.rglob("*.tst"))

    all_results = []
    error_count = 0

    for file_path in files:
        diagnostics = validate_tst(file_path)
        error_count += sum(1 for d in diagnostics if d.severity == "error")
        all_results.append({"path": str(file_path), "diagnostics": diagnostics})

    print(json.dumps(dataclass_to_dict(all_results), indent=2))
    return 1 if error_count else 0


def cmd_inspect_reviewids(args: argparse.Namespace) -> int:
    loader = ReviewIdXlsmLoader(args.path)
    print(json.dumps(loader.inspect(), indent=2))
    return 0


def cmd_inspect_eapx(args: argparse.Namespace) -> int:
    print(json.dumps(inspect_eapx(args.path), indent=2))
    return 0


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="vcastgen")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init-config")
    p.add_argument("--output", default="vcastgen.yaml")
    p.set_defaults(func=cmd_init_config)

    p = sub.add_parser("parse")
    p.add_argument("--config", default="vcastgen.yaml")
    p.set_defaults(func=cmd_parse)

    p = sub.add_parser("generate")
    p.add_argument("--config", default="vcastgen.yaml")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_generate)

    p = sub.add_parser("validate")
    p.add_argument("path")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("inspect-reviewids")
    p.add_argument("path")
    p.set_defaults(func=cmd_inspect_reviewids)

    p = sub.add_parser("inspect-eapx")
    p.add_argument("path")
    p.set_defaults(func=cmd_inspect_eapx)

    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()
    return args.func(args)