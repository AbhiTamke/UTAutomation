from __future__ import annotations

from vcast_automation.diagnostics.codes import (
    PLAN_BRANCH_TARGET_NOT_GUARANTEED,
    PLAN_EXPECTED_VALUE_NOT_PROVEN,
    PLAN_TEST_LIMIT_REACHED,
)
from vcast_automation.models.core import Diagnostic, FunctionModel, SourceFileModel, TestCasePlan


def _safe_value_for_type(type_name: str, is_pointer: bool, is_array: bool) -> str | None:
    """
    Conservative safe scalar placeholder policy.

    Do not emit scalar placeholders for pointers/arrays. VectorCAST pointer/array
    setup should be explicit through raw_value_lines or project rules.
    """
    if is_pointer or is_array:
        return None

    normalized = type_name.lower().replace(" ", "")

    if normalized in {
        "int",
        "short",
        "long",
        "uint8",
        "uint8_t",
        "uint16",
        "uint16_t",
        "uint32",
        "uint32_t",
        "sint8",
        "sint8_t",
        "sint16",
        "sint16_t",
        "sint32",
        "sint32_t",
    }:
        return "0"

    if normalized in {"bool", "boolean"}:
        return "false"

    if normalized == "char":
        return "'A'"

    return None


class TestPlanner:
    def __init__(self, config: dict):
        self.config = config
        self.generation = config.get("generation", {})

    def plan_source(self, source: SourceFileModel) -> list[TestCasePlan]:
        if self.generation.get("enable_project_rules", False):
            try:
                from vcast_automation.planner.vectorcast_value_rules import load_reference_test_plans

                reference_plans = load_reference_test_plans(source, self.config)
                if reference_plans is not None:
                    return reference_plans
            except Exception:
                pass

        plans: list[TestCasePlan] = []

        for fn in source.functions:
            function_plans: list[TestCasePlan] = []
            index = 1

            if self.generation.get("enable_baseline_cases", True):
                function_plans.append(
                    self._make_case(
                        fn=fn,
                        family="baseline",
                        index=index,
                        description=f"Baseline skeleton test for function {fn.function_name}.",
                        coverage_intent="Baseline execution intent.",
                    )
                )
                index += 1

            if self.generation.get("enable_condition_cases", True):
                for condition in fn.conditions:
                    condition_text = condition.expression.strip()
                    if not condition_text:
                        condition_text = f"condition at line {condition.line_start}"

                    function_plans.append(
                        self._make_case(
                            fn=fn,
                            family="condition_true",
                            index=index,
                            description=f"Targets true branch of condition {condition_text}.",
                            coverage_intent=f"Intent-only true branch for condition at line {condition.line_start}.",
                        )
                    )
                    function_plans[-1].diagnostics.append(
                        Diagnostic(
                            code=PLAN_BRANCH_TARGET_NOT_GUARANTEED,
                            message="Branch target is intent-only; no guaranteed input solving is performed.",
                        )
                    )
                    index += 1

                    function_plans.append(
                        self._make_case(
                            fn=fn,
                            family="condition_false",
                            index=index,
                            description=f"Targets false branch of condition {condition_text}.",
                            coverage_intent=f"Intent-only false branch for condition at line {condition.line_start}.",
                        )
                    )
                    function_plans[-1].diagnostics.append(
                        Diagnostic(
                            code=PLAN_BRANCH_TARGET_NOT_GUARANTEED,
                            message="Branch target is intent-only; no guaranteed input solving is performed.",
                        )
                    )
                    index += 1

            if self.generation.get("enable_switch_cases", True):
                for switch_case in fn.switch_cases:
                    family = "switch_default" if switch_case.is_default else f"switch_{switch_case.label}"
                    function_plans.append(
                        self._make_case(
                            fn=fn,
                            family=family,
                            index=index,
                            description=f"Targets switch case {switch_case.label}.",
                            coverage_intent=f"Intent-only switch case coverage for {switch_case.label}.",
                        )
                    )
                    index += 1

            if self.generation.get("enable_loop_cases", True):
                for loop in fn.loops:
                    for loop_family in ("loop_zero", "loop_one", "loop_many"):
                        function_plans.append(
                            self._make_case(
                                fn=fn,
                                family=loop_family,
                                index=index,
                                description=f"Targets {loop_family} intent for {loop.kind} loop.",
                                coverage_intent=f"Intent-only loop path for {loop.kind} at line {loop.line_number}.",
                            )
                        )
                        index += 1

            max_tests = int(self.generation.get("max_tests_per_function", 20))
            if len(function_plans) > max_tests:
                kept = function_plans[:max_tests]
                kept[-1].diagnostics.append(
                    Diagnostic(
                        code=PLAN_TEST_LIMIT_REACHED,
                        message=f"Function test count exceeded max_tests_per_function={max_tests}; extra cases skipped.",
                    )
                )
                function_plans = kept

            plans.extend(function_plans)

        return plans

    def _make_case(
        self,
        fn: FunctionModel,
        family: str,
        index: int,
        description: str,
        coverage_intent: str,
    ) -> TestCasePlan:
        pattern = self.generation.get("test_naming_pattern", "{unit}_{function}_{family}_{index:03d}")
        test_name = pattern.format(
            unit=fn.unit_name,
            function=fn.function_name,
            family=family,
            index=index,
        )

        input_values: dict[str, str] = {}
        notes: list[str] = []

        for param in fn.parameters:
            value = _safe_value_for_type(param.type, param.is_pointer, param.is_array)
            if value is None:
                notes.append(
                    f"Parameter {param.name} of type {param.type} requires explicit/manual VectorCAST assignment."
                )
                continue
            input_values[param.name] = value

        plan = TestCasePlan(
            test_case_id=test_name,
            test_name=test_name,
            unit_name=fn.unit_name,
            subprogram_name=fn.vcast_subprogram_name,
            source_path=fn.source_path,
            function_name=fn.function_name,
            family=family,
            description=description,
            coverage_intent=coverage_intent,
            input_values=input_values,
            status=self.generation.get("default_status", "Draft"),
            asil=list(self.generation.get("default_asil", ["QM"])),
            priority=self.generation.get("default_priority", "High"),
            notes=" ".join(notes),
            generation_mode=self.generation.get("mode", "skeleton"),
            generation_reason="static parser planning",
            parser_confidence=fn.parser_confidence,
            diagnostics=[
                Diagnostic(
                    code=PLAN_EXPECTED_VALUE_NOT_PROVEN,
                    message="TEST.EXPECTED omitted unless supplied by explicit mapping/rule.",
                )
            ],
        )

        if self.generation.get("enable_project_rules", False):
            try:
                from vcast_automation.planner.vectorcast_value_rules import apply_app_sli_known_rules

                apply_app_sli_known_rules(plan, fn, self.config)
            except Exception as exc:
                plan.notes = (plan.notes + f" Project rule enrichment skipped: {exc}").strip()

        return plan