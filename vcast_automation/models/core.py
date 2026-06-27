from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Diagnostic:
    code: str
    message: str
    severity: str = "warning"
    source: str | None = None


@dataclass
class ParameterModel:
    name: str
    type: str = "int"
    direction: str = "in"
    is_pointer: bool = False
    is_reference: bool = False
    is_const: bool = False
    is_array: bool = False
    is_struct: bool = False
    is_enum: bool = False
    default_value: str | None = None
    safe_placeholder_value: str | None = None
    value_confidence: str = "low"
    diagnostics: list[Diagnostic] = field(default_factory=list)
    # New fields for richer generation and safety
    base_type: str = ""
    pointer_depth: int = 0
    array_length_param: str = ""
    size_dependency_on: str = ""
    enum_values: list[str] = field(default_factory=list)
    domain_min: str | None = None
    domain_max: str | None = None
    allow_null: bool = False
    allow_nan: bool = False
    allow_inf: bool = False
    allow_invalid_enum: bool = False
    alias_group: str = ""
    dependency_tags: list[str] = field(default_factory=list)


@dataclass
class ConditionModel:
    expression: str
    normalized_expression: str = ""
    kind: str = "if"
    line_start: int = 0
    line_end: int = 0
    branch_intents: list[str] = field(default_factory=lambda: ["true", "false"])
    referenced_parameters: list[str] = field(default_factory=list)
    referenced_globals: list[str] = field(default_factory=list)
    referenced_constants: list[str] = field(default_factory=list)
    calls_inside_condition: list[str] = field(default_factory=list)
    parser_confidence: str = "medium"
    input_confidence: str = "low"
    coverage_confidence: str = "intent-only"
    diagnostics: list[Diagnostic] = field(default_factory=list)
    # New fields for extracted constraints
    operator: str = ""
    lhs_symbol: str = ""
    rhs_literal: str = ""
    constraint_candidates: list[str] = field(default_factory=list)
    is_potentially_unreachable: bool = False
    unreachable_reason: str = ""


@dataclass
class SwitchCaseModel:
    label: str
    is_default: bool = False
    line_number: int = 0


@dataclass
class LoopModel:
    kind: str
    condition: str = ""
    line_number: int = 0


@dataclass
class FunctionModel:
    source_path: str
    unit_name: str
    function_name: str
    qualified_name: str
    vcast_subprogram_name: str
    return_type: str
    signature: str
    parameters: list[ParameterModel] = field(default_factory=list)
    globals_read: list[str] = field(default_factory=list)
    globals_written: list[str] = field(default_factory=list)
    calls: list[str] = field(default_factory=list)
    internal_calls: list[str] = field(default_factory=list)
    external_calls: list[str] = field(default_factory=list)
    unresolved_calls: list[str] = field(default_factory=list)
    conditions: list[ConditionModel] = field(default_factory=list)
    loops: list[LoopModel] = field(default_factory=list)
    switch_cases: list[SwitchCaseModel] = field(default_factory=list)
    return_paths: int = 0
    line_start: int = 0
    line_end: int = 0
    is_static: bool = False
    is_public: bool = False
    is_class_method: bool = False
    class_name: str = ""
    namespace: str = ""
    parser_backend: str = "lightweight"
    parser_confidence: str = "medium"
    qualification_confidence: str = "low"
    diagnostics: list[Diagnostic] = field(default_factory=list)
    # New fields for analysis/planning support
    static_state_vars: list[str] = field(default_factory=list)
    input_dependencies: list[dict[str, str]] = field(default_factory=list)
    probe_points: list[str] = field(default_factory=list)
    environment_tags: list[str] = field(default_factory=list)
    stub_targets: list[str] = field(default_factory=list)


@dataclass
class SourceFileModel:
    source_path: str
    source_stem: str
    unit_name: str
    language: str = "unknown"
    parser_backend: str = "lightweight"
    parser_confidence: str = "medium"
    includes: list[str] = field(default_factory=list)
    macros: list[str] = field(default_factory=list)
    globals: list[str] = field(default_factory=list)
    types: list[str] = field(default_factory=list)
    enums: list[str] = field(default_factory=list)
    functions: list[FunctionModel] = field(default_factory=list)
    diagnostics: list[Diagnostic] = field(default_factory=list)
    # New fields for execution/config metadata
    compiler_profile: dict[str, str] = field(default_factory=dict)
    environment_name: str = ""
    cfg_path: str = ""
    env_path: str = ""


@dataclass
class TraceabilityRecord:
    test_case_id: str = ""
    unit: str = ""
    function: str = ""
    subprogram: str = ""
    requirement_key: str = ""
    review_id: str = ""
    guid: str = ""
    status: str = ""
    asil: str = ""
    notes: str = ""
    description: str = ""
    source: str = ""
    match_confidence: str = "none"
    match_status: str = "missing"
    # New fields for traceability clarity
    rule_source: str = ""
    override_source: str = ""
    seed: str = ""
    coverage_target: str = ""


@dataclass
class TestCasePlan:
    test_case_id: str
    test_name: str
    unit_name: str
    subprogram_name: str
    source_path: str
    function_name: str
    family: str
    description: str
    coverage_intent: str

    # Simple parameter values, rendered as Unit.Subprogram.param:value.
    input_values: dict[str, str] = field(default_factory=dict)

    # Expected values, rendered exactly as TEST.EXPECTED:key:value.
    # These must come from explicit mappings or proven simple returns only.
    expected_values: dict[str, str] = field(default_factory=dict)

    # Advanced writer controls.
    raw_value_lines: list[str] = field(default_factory=list)
    stub_lines: list[str] = field(default_factory=list)
    raw_expected_lines: list[str] = field(default_factory=list)

    expected_confidence: str = "none"
    requirement_keys: list[str] = field(default_factory=list)
    review_id: str = "TBD"
    guid: str = "TBD"
    status: str = "Draft"
    asil: list[str] = field(default_factory=lambda: ["QM"])
    priority: str = "High"
    notes: str = ""
    generation_mode: str = "skeleton"
    generation_reason: str = ""
    parser_confidence: str = "medium"
    input_confidence: str = "low"
    coverage_confidence: str = "intent-only"
    traceability_status: str = "unresolved"
    diagnostics: list[Diagnostic] = field(default_factory=list)
    # New fields for staged generation, safety, dependencies, and advanced features
    generation_stage: str = "baseline"
    feedback_iteration: int = 0
    seed: int | None = None
    safety_profile_name: str = ""
    environment_profile_name: str = ""
    dependency_edges: list[str] = field(default_factory=list)
    rejected_values: list[str] = field(default_factory=list)
    pointer_setup_lines: list[str] = field(default_factory=list)
    global_init_lines: list[str] = field(default_factory=list)
    state_restore_lines: list[str] = field(default_factory=list)
    stub_profile: str = ""
    stub_behavior_lines: list[str] = field(default_factory=list)
    validator_messages: list[str] = field(default_factory=list)
    coverage_targets: list[str] = field(default_factory=list)
    template_version: str = "v1"
    override_source: str = ""
    rule_source: str = ""
    is_negative_test: bool = False
    requires_manual_review: bool = False


@dataclass
class TstDocument:
    output_path: str
    source_path: str
    unit_name: str
    test_cases: list[TestCasePlan]
    header: str = ""
    script_features: list[str] = field(default_factory=list)
    diagnostics: list[Diagnostic] = field(default_factory=list)
    validation_status: str = "not_run"
    # New fields for artifact references and validation state
    env_output_path: str = ""
    cfg_output_path: str = ""
    execution_summary: dict[str, str] = field(default_factory=dict)
    coverage_summary: dict[str, str] = field(default_factory=dict)


def dataclass_to_dict(obj: Any) -> Any:
    if isinstance(obj, Path):
        return str(obj)
    if hasattr(obj, "__dataclass_fields__"):
        return {key: dataclass_to_dict(value) for key, value in obj.__dict__.items()}
    if isinstance(obj, list):
        return [dataclass_to_dict(item) for item in obj]
    if isinstance(obj, dict):
        return {key: dataclass_to_dict(value) for key, value in obj.items()}
    return obj