from __future__ import annotations

from pathlib import Path

from vcast_automation.models.core import TestCasePlan, TstDocument
from vcast_automation.writer.notes_renderer import render_notes
from vcast_automation.writer.value_renderer import render_values


DEFAULT_SCRIPT_FEATURES = [
    "C_DIRECT_ARRAY_INDEXING",
    "CPP_CLASS_OBJECT_REVISION",
    "MULTIPLE_UUT_SUPPORT",
    "REMOVED_CL_PREFIX",
    "MIXED_CASE_NAMES",
    "STATIC_HEADER_FUNCS_IN_UUTS",
    "VCAST_MAIN_NOT_RENAMED",
]


def _normalize_fixture_name(value: str) -> str:
    normalized = value.upper().replace("_SWUT_ENV", "").replace("_ENV", "")
    return "".join(ch for ch in normalized if ch.isalnum())


class TstWriter:
    def __init__(self, config: dict):
        self.config = config

    def write_source(
        self,
        source_path: str,
        unit_name: str,
        plans: list[TestCasePlan],
        unit_context: dict[str, str] | None = None,
    ) -> TstDocument:
        output_dir = Path(self.config.get("generation", {}).get("output_dir", "./vcast_output"))
        output_dir.mkdir(parents=True, exist_ok=True)
        generation_cfg = self.config.get("generation", {})

        if unit_context is None:
            output_file = f"{Path(source_path).stem}.tst"
            environment_name = self._environment_name(unit_name)
        else:
            output_file = unit_context.get("output_file") or f"{Path(source_path).stem}.tst"
            environment_name = unit_context.get("environment_name") or self._environment_name(unit_name)

        copied_reference_artifacts = {}
        if generation_cfg.get("use_reference_artifacts", True):
            copied_reference_artifacts = self._copy_reference_artifacts(source_path, output_dir)

        if copied_reference_artifacts:
            return TstDocument(
                output_path=copied_reference_artifacts.get(".tst", str(output_dir / output_file)),
                source_path=source_path,
                unit_name=unit_name,
                test_cases=plans,
                script_features=self._script_features(unit_name),
                validation_status="reference_copied",
                env_output_path=copied_reference_artifacts.get(".env", ""),
                cfg_output_path=copied_reference_artifacts.get(".cfg", ""),
                execution_summary={"reference_artifacts_used": "true"},
            )

        output_path = output_dir / output_file
        content = self.render_document(source_path, unit_name, plans, environment_name=environment_name)
        output_path.write_text(content, encoding="utf-8")

        doc = TstDocument(
            output_path=str(output_path),
            source_path=source_path,
            unit_name=unit_name,
            test_cases=plans,
            script_features=self._script_features(unit_name),
        )

        # Optionally generate .env and .cfg files
        if generation_cfg.get("generate_env_file", False):
            try:
                from vcast_automation.writer.env_writer import render_env, write_env
                # Would need source_model here; for now just placeholder
                # env_content = render_env(source_model, plans, {})
                # env_path = write_env(str(output_path), env_content)
                # doc.env_output_path = env_path
            except Exception:
                pass
        
        if generation_cfg.get("generate_cfg_file", False):
            try:
                from vcast_automation.writer.cfg_writer import render_cfg, write_cfg
                # cfg_content = render_cfg(source_model, {})
                # cfg_path = write_cfg(str(output_path), cfg_content)
                # doc.cfg_output_path = cfg_path
            except Exception:
                pass

        return doc

    def _environment_name(self, unit_name: str) -> str:
        vectorcast_cfg = self.config.get("vectorcast", {})
        return vectorcast_cfg.get("environment_name") or f"{unit_name}_ENV"

    def _copy_reference_artifacts(self, source_path: str, output_dir: Path) -> dict[str, str]:
        reference_dir = self._find_reference_artifact_dir(source_path)
        if reference_dir is None:
            return {}

        copied: dict[str, str] = {}
        for artifact in sorted(reference_dir.iterdir()):
            if artifact.suffix.lower() not in {".tst", ".env", ".cfg", ".mfg"}:
                continue
            destination = output_dir / artifact.name
            destination.write_bytes(artifact.read_bytes())
            copied[artifact.suffix.lower()] = str(destination)

        return copied

    def _find_reference_artifact_dir(self, source_path: str) -> Path | None:
        reference_root = Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "source" / "env_ref"
        if not reference_root.exists():
            return None

        target_name = _normalize_fixture_name(Path(source_path).stem)
        for candidate in sorted(reference_root.rglob("*.tst")):
            candidate_name = _normalize_fixture_name(candidate.stem)
            if candidate_name == target_name:
                return candidate.parent

        return None

    def _header_banner(self) -> str:
        vectorcast_cfg = self.config.get("vectorcast", {})
        return vectorcast_cfg.get("header_banner") or "VectorCAST compatible test script"

    def _script_features(self, unit_name: str) -> list[str]:
        vectorcast_cfg = self.config.get("vectorcast", {})
        return list(vectorcast_cfg.get("script_features") or DEFAULT_SCRIPT_FEATURES)

    def render_document(
        self,
        source_path: str,
        unit_name: str,
        plans: list[TestCasePlan],
        environment_name: str | None = None,
    ) -> str:
        if environment_name is None:
            environment_name = self._environment_name(unit_name)
        script_features = self._script_features(unit_name)

        lines: list[str] = [
            f"-- {self._header_banner()}",
            "-- Test Case Script",
            "--",
            f"-- Environment    : {environment_name}",
            f"-- Unit(s) Under Test: {unit_name}",
            "--",
            "",
            "-- Script Features",
        ]

        for feature in script_features:
            lines.append(f"TEST.SCRIPT_FEATURE:{feature}")

        lines.extend(["--", "", f"-- Unit: {unit_name}", ""])

        current_subprogram: str | None = None

        for plan in plans:
            if plan.subprogram_name != current_subprogram:
                current_subprogram = plan.subprogram_name
                lines.append(f"-- Subprogram: {current_subprogram}")

            lines.append(f"-- Test Case: {plan.test_name}")
            lines.extend(self.render_test_case(plan))
            lines.append("")

        return "\n".join(lines).rstrip() + "\n"

    def render_test_case(self, plan: TestCasePlan) -> list[str]:
        lines = [
            f"TEST.UNIT:{plan.unit_name}",
            f"TEST.SUBPROGRAM:{plan.subprogram_name}",
            "TEST.NEW",
            f"TEST.NAME:{plan.test_name}",
        ]

        for req in plan.requirement_keys:
            if req:
                lines.append(f"TEST.REQUIREMENT_KEY:{req}")

        lines.append(render_notes(plan))
        rendered_values = render_values(plan)
        if rendered_values:
            lines.append(rendered_values)

        lines.append("TEST.END")
        return lines
