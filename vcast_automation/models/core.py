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