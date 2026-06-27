from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class CallType(str, Enum):
    UNRESOLVED = "unresolved"
    INTERNAL = "internal"
    EXTERNAL = "external"


class StmtKind(str, Enum):
    SIMPLE = "simple"
    CALL = "call"
    IF = "if"
    LOOP = "loop"
    SWITCH = "switch"
    RETURN = "return"


@dataclass
class IncludeInfo:
    target: str
    is_system: bool = False
    file_path: str = ""
    line_number: int = 0


@dataclass
class VariableInfo:
    name: str
    type: str = ""
    is_static: bool = False
    is_const: bool = False
    is_macro: bool = False
    initial_value: str = ""
    file_path: str = ""
    line_number: int = 0


@dataclass
class ParameterInfo:
    name: str
    type: str = "int"
    is_pointer: bool = False
    is_reference: bool = False
    is_const: bool = False
    is_array: bool = False


@dataclass
class EnumInfo:
    name: str
    values: list[str] = field(default_factory=list)
    file_path: str = ""
    line_number: int = 0


@dataclass
class StructInfo:
    name: str
    kind: str = "struct"
    fields: list[ParameterInfo] = field(default_factory=list)
    file_path: str = ""
    line_number: int = 0


@dataclass
class TypedefInfo:
    name: str
    underlying_type: str = ""
    file_path: str = ""
    line_number: int = 0


@dataclass
class SwitchCase:
    label: str
    is_default: bool = False


@dataclass
class ControlConstruct:
    kind: str
    condition: str = ""
    line_number: int = 0
    summary: str = ""


@dataclass
class CallInfo:
    caller: str
    callee: str
    call_type: CallType = CallType.UNRESOLVED
    arguments: list[str] = field(default_factory=list)
    line_number: int = 0


@dataclass
class PreprocessorBlock:
    condition: str
    line_start: int
    line_end: int


@dataclass
class Statement:
    kind: StmtKind
    line: int = 0
    text: str = ""
    condition: str = ""
    loop_kind: str = ""
    return_value: str = ""
    calls: list[str] = field(default_factory=list)
    assigned: list[str] = field(default_factory=list)
    body: list["Statement"] = field(default_factory=list)
    else_body: list["Statement"] = field(default_factory=list)
    cases: list[SwitchCase] = field(default_factory=list)


@dataclass
class FunctionInfo:
    name: str
    qualified_name: str
    signature: str
    return_type: str
    parameters: list[ParameterInfo] = field(default_factory=list)
    file_path: str = ""
    line_start: int = 0
    line_end: int = 0
    is_static: bool = False
    is_declaration_only: bool = False
    body: str = ""
    calls: list[CallInfo] = field(default_factory=list)
    control_constructs: list[ControlConstruct] = field(default_factory=list)
    conditions: list[ControlConstruct] = field(default_factory=list)
    loops: list[ControlConstruct] = field(default_factory=list)
    switch_cases: list[SwitchCase] = field(default_factory=list)
    return_paths: int = 0
    preprocessor_conditions: list[str] = field(default_factory=list)
    preprocessor_blocks: list[PreprocessorBlock] = field(default_factory=list)
    body_block: list[Statement] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    parser_confidence: str = "medium"


@dataclass
class ParsedFile:
    path: str
    is_header: bool = False
    parser_used: str = ""
    parse_ok: bool = True
    warnings: list[str] = field(default_factory=list)
    includes: list[IncludeInfo] = field(default_factory=list)
    macros: list[VariableInfo] = field(default_factory=list)
    enums: list[EnumInfo] = field(default_factory=list)
    structs: list[StructInfo] = field(default_factory=list)
    typedefs: list[TypedefInfo] = field(default_factory=list)
    variables: list[VariableInfo] = field(default_factory=list)
    functions: list[FunctionInfo] = field(default_factory=list)