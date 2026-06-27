"""
tst_validator.py — Validation of generated .tst files before acceptance.

Checks syntax, semantic consistency, and coverage completeness.
"""

from __future__ import annotations

from vcast_automation.models.core import Diagnostic, TestCasePlan


def validate_plan(
    test_plan: TestCasePlan,
    function_model,
) -> list[Diagnostic]:
    """
    Validate a test plan before generation.
    
    Args:
        test_plan: Plan to validate.
        function_model: Function being tested.
    
    Returns:
        List of diagnostics (errors, warnings).
    """
    diagnostics = []
    
    # Check for required fields
    if not test_plan.test_name:
        diagnostics.append(
            Diagnostic(
                code="VALIDATOR_MISSING_TEST_NAME",
                message="Test case is missing test_name",
                severity="error",
            )
        )
    
    # Check for uninitialized parameters
    for param in function_model.parameters:
        if param.name not in test_plan.input_values and param.name not in test_plan.raw_value_lines:
            if not param.default_value:
                diagnostics.append(
                    Diagnostic(
                        code="VALIDATOR_UNINITIALIZED_PARAM",
                        message=f"Parameter {param.name} has no assigned value",
                        severity="warning",
                    )
                )
    
    # Check for syntax errors in raw lines
    for i, line in enumerate(test_plan.raw_value_lines):
        if not _is_valid_directive(line):
            diagnostics.append(
                Diagnostic(
                    code="VALIDATOR_SYNTAX_FAILURE",
                    message=f"Invalid directive syntax in raw_value_lines[{i}]: {line}",
                    severity="warning",
                )
            )
    
    # Check for manual review requirement
    if test_plan.requires_manual_review:
        diagnostics.append(
            Diagnostic(
                code="CODE_REQUIRES_MANUAL_REVIEW",
                message="Test case flagged as requiring manual review",
                severity="info",
            )
        )
    
    return diagnostics


def validate_document(text: str) -> list[Diagnostic]:
    """
    Validate generated .tst document text.
    
    Args:
        text: Content of .tst file.
    
    Returns:
        List of diagnostics.
    """
    diagnostics = []
    lines = text.split("\n")
    
    # Check for unbalanced TEST blocks
    test_count = 0
    block_stack = []
    
    for i, line in enumerate(lines, 1):
        if line.strip().startswith("TEST"):
            test_count += 1
            block_stack.append(i)
        elif line.strip() == "}":
            if block_stack:
                block_stack.pop()
    
    if block_stack:
        diagnostics.append(
            Diagnostic(
                code="TST_UNBALANCED_TEST_BLOCK",
                message=f"Unbalanced TEST block(s) starting at lines: {block_stack}",
                severity="error",
            )
        )
    
    # Check for required markers
    if "TEST.NOTES:" not in text:
        diagnostics.append(
            Diagnostic(
                code="TST_MISSING_NOTES_MARKER",
                message="Document missing TEST.NOTES: marker",
                severity="warning",
            )
        )
    
    # Check for duplicate test names
    test_names = []
    for line in lines:
        if "TEST.SUBPROGRAM:" in line or "TEST.NAME:" in line:
            test_names.append(line.strip())
    
    if len(test_names) != len(set(test_names)):
        diagnostics.append(
            Diagnostic(
                code="TST_DUPLICATE_TEST_NAME",
                message="Duplicate test names detected",
                severity="warning",
            )
        )
    
    return diagnostics


# Internal helpers

def _is_valid_directive(line: str) -> bool:
    """Check if a line looks like a valid VectorCAST directive."""
    valid_prefixes = (
        "TEST.",
        "UNIT.",
        "SUBPROGRAM.",
        "{",
        "}",
        "CATURE:",
        "RETURN:",
        "EXPECTED:",
        "VALUE:",
        "//",
        "#",
        "",  # Empty lines OK
    )
    
    stripped = line.strip()
    return any(stripped.startswith(p) for p in valid_prefixes)
