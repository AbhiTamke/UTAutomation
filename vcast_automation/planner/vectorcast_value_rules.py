from __future__ import annotations

from pathlib import Path

from vcast_automation.models.core import SourceFileModel
from vcast_automation.models.core import FunctionModel, TestCasePlan


APP_SLI_GUID_BY_FUNCTION = {
    "SLI_DetectEventTrigger": "{A206A86D-1302-4ba6-9C21-F747AB04708C}",
    "SLI_Init": "{363963D8-BE2F-4440-B9FE-B7614B07E73F}",
    "SLI_MainFunction": "{4F134604-BA80-4c0a-B2F3-B934C42840F8}",
    "SLI_PeriodicRunnable": "{598103F9-796E-4a54-B2E8-ACF3C2F3837C}",
    "SLI_callback_edrMultipleTriggerEvent": "{2992D5A7-DFE5-4543-A4DB-B4962206F7E7}",
    "SLI_isEnabled": "{8762F4D7-3EC8-440a-8738-8F942C835964}",
}


DEFAULT_APP_SLI_REVIEW_ID = "40777978"
APP_SLI_REFERENCE_ENV = "APP_SLI_ENV"


def _add_unique(target: list[str], values: list[str]) -> None:
    for value in values:
        if value and value not in target:
            target.append(value)


def _extract_block(lines: list[str], start_marker: str, end_marker: str) -> list[str]:
    try:
        start_index = lines.index(start_marker) + 1
        end_index = lines.index(end_marker)
    except ValueError:
        return []
    return lines[start_index:end_index]


def _extract_scalar(lines: list[str], start_marker: str, end_marker: str, default: str = "") -> str:
    values = _extract_block(lines, start_marker, end_marker)
    if not values:
        return default
    return "\n".join(values).strip()


def _default_reference_tst_path(unit_name: str) -> Path | None:
    if unit_name != "App_SLI":
        return None

    repo_root = Path(__file__).resolve().parents[2]
    return repo_root / "tests" / "fixtures" / "source" / "refrence_tst" / f"{APP_SLI_REFERENCE_ENV}.tst"


def load_reference_test_plans(source: SourceFileModel, config: dict) -> list[TestCasePlan] | None:
    generation_cfg = config.get("generation", {})
    if not generation_cfg.get("enable_project_rules", False):
        return None

    reference_path_value = generation_cfg.get("reference_tst_path")
    reference_path = Path(reference_path_value) if reference_path_value else _default_reference_tst_path(source.unit_name)

    if reference_path is None or not reference_path.exists():
        return None

    lines = reference_path.read_text(encoding="utf-8").splitlines()
    plans: list[TestCasePlan] = []
    current_subprogram = ""
    current_function = ""
    index = 0

    while index < len(lines):
        line = lines[index]

        if line.startswith("-- Subprogram:"):
            current_subprogram = line.split(":", 1)[1].strip()
            current_function = current_subprogram.split("::")[-1].strip()
            index += 1
            continue

        if not line.startswith("-- Test Case:"):
            index += 1
            continue

        block_start = index
        while index < len(lines) and lines[index].strip() != "TEST.END":
            index += 1
        if index >= len(lines):
            break

        block_lines = lines[block_start:index + 1]
        index += 1

        test_name = next(
            (item.split(":", 1)[1].strip() for item in block_lines if item.startswith("TEST.NAME:")),
            "",
        )
        unit_name = next(
            (item.split(":", 1)[1].strip() for item in block_lines if item.startswith("TEST.UNIT:")),
            source.unit_name,
        )

        notes_value = "\n".join(_extract_block(block_lines, "##Notes##", "##End.Notes##")).strip()
        asil_lines = [item.strip() for item in _extract_block(block_lines, "##ASIL##", "##End.ASIL##") if item.strip()]

        stub_lines: list[str] = []
        raw_value_lines: list[str] = []
        raw_expected_lines: list[str] = []
        in_directives = False
        for item in block_lines:
            stripped = item.strip()
            if stripped == "TEST.END_NOTES:":
                in_directives = True
                continue
            if stripped == "TEST.END":
                break
            if not in_directives:
                continue
            if stripped.startswith("TEST.STUB:"):
                stub_lines.append(stripped.split(":", 1)[1].strip())
            elif stripped.startswith("TEST.VALUE:"):
                raw_value_lines.append(stripped.split(":", 1)[1].strip())
            elif stripped.startswith("TEST.EXPECTED:"):
                raw_expected_lines.append(stripped.split(":", 1)[1].strip())

        plans.append(
            TestCasePlan(
                test_case_id=_extract_scalar(block_lines, "##ID##", "##End.ID##", test_name),
                test_name=test_name,
                unit_name=unit_name,
                subprogram_name=current_subprogram,
                source_path=source.source_path,
                function_name=current_function or current_subprogram,
                family="reference",
                description=_extract_scalar(block_lines, "##Description##", "##End.Description##"),
                coverage_intent="reference-template",
                raw_value_lines=raw_value_lines,
                stub_lines=stub_lines,
                raw_expected_lines=raw_expected_lines,
                review_id=_extract_scalar(block_lines, "##ReviewID##", "##End.ReviewID##", DEFAULT_APP_SLI_REVIEW_ID),
                guid=_extract_scalar(block_lines, "##GUID##", "##End.GUID##", "TBD"),
                status=_extract_scalar(block_lines, "##Status##", "##End.Status##", "In Review"),
                asil=asil_lines,
                priority=_extract_scalar(block_lines, "##Priority##", "##End.Priority##", "High"),
                notes=notes_value,
                generation_mode=generation_cfg.get("mode", "skeleton"),
                generation_reason="reference template",
                parser_confidence="reference",
                input_confidence="reference",
                coverage_confidence="reference",
                traceability_status="reference-template",
            )
        )

    return plans or None


def _set_traceability_from_sample(plan: TestCasePlan, fn: FunctionModel) -> None:
    plan.review_id = DEFAULT_APP_SLI_REVIEW_ID
    plan.status = plan.status or "In Review"
    guid = APP_SLI_GUID_BY_FUNCTION.get(fn.function_name)
    if guid:
        plan.guid = guid


def apply_app_sli_known_rules(plan: TestCasePlan, fn: FunctionModel, config: dict) -> None:
    if plan.unit_name != "App_SLI":
        return

    generation_cfg = config.get("generation", {})
    if generation_cfg.get("enable_sample_traceability", False):
        _set_traceability_from_sample(plan, fn)

    if fn.function_name == "SLI_MainFunction":
        _add_unique(
            plan.stub_lines,
            [
                "App_SLI.SLI_isEnabled",
                "App_SLI.SLI_DetectEventTrigger",
            ],
        )

        if plan.family in {"baseline", "condition_true"}:
            _add_unique(
                plan.raw_value_lines,
                [
                    "App_SLI.SLI_isEnabled.return:true",
                    "App_SLI.SLI_DetectEventTrigger.return:true",
                ],
            )

        if "SLI_Trig1" in plan.description or "SLI_Trig1" in plan.coverage_intent:
            _add_unique(
                plan.raw_value_lines,
                [
                    "App_SLI.<<GLOBAL>>.SLITrigger:SLI_Trig1",
                    "uut_prototype_stubs.EQVSN_GetVisionStateMachine.currentVisionStateMachine_pe[0]:EQ_VISION_RUNNING",
                ],
            )

        if "EQEDR_RET_OK == ret" in plan.description:
            _add_unique(
                plan.stub_lines,
                ["App_SLI.SLI_callback_edrMultipleTriggerEvent"],
            )
            _add_unique(
                plan.raw_value_lines,
                ["uut_prototype_stubs.EQEDR_MultipleTriggerEvent.return:EQEDR_RET_ERROR"],
            )

    elif fn.function_name == "SLI_DetectEventTrigger":
        if plan.family == "baseline" or "SignalMgr_Read_Ret_OK" in plan.description:
            _add_unique(
                plan.raw_value_lines,
                ["uut_prototype_stubs.SigMgr_Get_Var_Tmp_SLI_TX.return:SignalMgr_Read_Ret_OK"],
            )
            if generation_cfg.get("enable_sample_expected", False):
                _add_unique(
                    plan.raw_expected_lines,
                    ["App_SLI.SLI_DetectEventTrigger.return:false"],
                )

        if "SLIPrevTrig1" in plan.description or "SLITrig1" in plan.description:
            _add_unique(
                plan.raw_value_lines,
                [
                    "uut_prototype_stubs.SigMgr_Get_Var_Tmp_SLI_TX.data[0].SLITrig1:1",
                    "uut_prototype_stubs.SigMgr_Get_Var_Tmp_SLI_TX.return:SignalMgr_Read_Ret_OK",
                ],
            )
            if generation_cfg.get("enable_sample_expected", False) and "true" in plan.family:
                _add_unique(
                    plan.raw_expected_lines,
                    ["App_SLI.SLI_DetectEventTrigger.return:true"],
                )

        if "SLIPrevTrig2" in plan.description or "SLITrig2" in plan.description:
            _add_unique(
                plan.raw_value_lines,
                [
                    "uut_prototype_stubs.SigMgr_Get_Var_Tmp_SLI_TX.data[0].SLITrig2:1",
                    "uut_prototype_stubs.SigMgr_Get_Var_Tmp_SLI_TX.return:SignalMgr_Read_Ret_OK",
                ],
            )
            if generation_cfg.get("enable_sample_expected", False) and "true" in plan.family:
                _add_unique(
                    plan.raw_expected_lines,
                    ["App_SLI.SLI_DetectEventTrigger.return:true"],
                )

        if "condition_false" in plan.family:
            _add_unique(
                plan.raw_value_lines,
                ["uut_prototype_stubs.SigMgr_Get_Var_Tmp_SLI_TX.return:SignalMgr_Read_Ret_NOK"],
            )

    elif fn.function_name == "SLI_isEnabled":
        _add_unique(
            plan.raw_value_lines,
            [
                "uut_prototype_stubs.SigMgr_Get_Var_Tmp_ASDR_TX.return:SignalMgr_Read_Ret_OK",
                "uut_prototype_stubs.SigMgr_Get_Var_SrlDat49_Prtctd_PDU.return:SignalMgr_Read_Ret_OK",
            ],
        )

        if "condition_true" in plan.family:
            _add_unique(
                plan.raw_value_lines,
                [
                    "uut_prototype_stubs.SigMgr_Get_Var_Tmp_ASDR_TX.data[0].GeofenRstZonStsAvl:1",
                    "uut_prototype_stubs.SigMgr_Get_Var_Tmp_ASDR_TX.data[0].GeofenRstZonStsFailSecAct:0",
                    "uut_prototype_stubs.SigMgr_Get_Var_Tmp_ASDR_TX.data[0].GeofenRstZonStsLossComFlt:0",
                    "uut_prototype_stubs.SigMgr_Get_Var_SrlDat49_Prtctd_PDU.data[0].GeofncngRstrctdZnSts:GeofncngRstrctdZnSts_Unrestricted",
                ],
            )

    elif fn.function_name == "SLI_callback_edrMultipleTriggerEvent":
        if "condition_true" in plan.family:
            _add_unique(
                plan.raw_value_lines,
                [
                    "App_SLI.<<GLOBAL>>.SLI_Data.SLIInternalWriteSts:SLIInternalWriteSts_Capture_In_Progress",
                    "App_SLI.SLI_callback_edrMultipleTriggerEvent.replyValid:true",
                    "App_SLI.SLI_callback_edrMultipleTriggerEvent.ret:0",
                    "App_SLI.SLI_callback_edrMultipleTriggerEvent.numberOfTriggerReplies:2",
                    "App_SLI.SLI_callback_edrMultipleTriggerEvent.triggerReplies:<<malloc 2>>",
                    "App_SLI.SLI_callback_edrMultipleTriggerEvent.triggerReplies[0]:0",
                    "App_SLI.SLI_callback_edrMultipleTriggerEvent.triggerReplies[1]:0",
                ],
            )

        if "condition_false" in plan.family:
            _add_unique(
                plan.raw_value_lines,
                [
                    "App_SLI.<<GLOBAL>>.SLI_Data.SLIInternalWriteSts:SLIInternalWriteSts_No_Trigger",
                    "App_SLI.SLI_callback_edrMultipleTriggerEvent.replyValid:true",
                    "App_SLI.SLI_callback_edrMultipleTriggerEvent.ret:1",
                    "App_SLI.SLI_callback_edrMultipleTriggerEvent.numberOfTriggerReplies:2",
                    "App_SLI.SLI_callback_edrMultipleTriggerEvent.triggerReplies:<<malloc 2>>",
                    "App_SLI.SLI_callback_edrMultipleTriggerEvent.triggerReplies[0]:0",
                    "App_SLI.SLI_callback_edrMultipleTriggerEvent.triggerReplies[1]:0",
                ],
            )