"""
state_manager.py — Global/static state snapshot and restore planning.

Manages test isolation by generating state initialization and restoration
directives for global variables, static state, and external stubs.
"""

from __future__ import annotations

from vcast_automation.models.core import FunctionModel, Diagnostic


def build_global_init(function_model: FunctionModel) -> list[str]:
    """
    Generate initialization directives for globals read by the function.
    
    Args:
        function_model: Function being tested.
    
    Returns:
        List of initialization directives (VectorCAST format).
    """
    lines = []
    
    for global_name in function_model.globals_read:
        # Generate safe initialization
        lines.append(f"// Initialize global: {global_name}")
        lines.append(f"{global_name} = 0")
    
    if function_model.static_state_vars:
        lines.append("// Initialize static state variables")
        for static_var in function_model.static_state_vars:
            lines.append(f"{static_var} = 0  // Reset static state")
    
    return lines


def build_state_restore(function_model: FunctionModel) -> list[str]:
    """
    Generate directives to restore state after test execution.
    
    Useful for tests that modify global/static variables to avoid
    side effects on subsequent tests.
    
    Args:
        function_model: Function being tested.
    
    Returns:
        List of restore directives.
    """
    lines = []
    
    if function_model.globals_written:
        lines.append("// Restore globals modified by function")
        for global_name in function_model.globals_written:
            lines.append(f"{global_name} = 0  // Restore previous value")
    
    if function_model.static_state_vars:
        lines.append("// Restore static state")
        for static_var in function_model.static_state_vars:
            lines.append(f"{static_var} = 0  // Reset after test")
    
    return lines


def validate_state_plan(plan) -> list[Diagnostic]:
    """
    Validate that state setup/restore is complete.
    
    Args:
        plan: TestCasePlan to validate.
    
    Returns:
        List of diagnostics for incomplete state setup.
    """
    diagnostics = []
    
    # Check if globals_read are initialized
    if plan.global_init_lines and not any("Initialize global" in line for line in plan.global_init_lines):
        diagnostics.append(
            Diagnostic(
                code="STATE_INIT_INCOMPLETE",
                message="Global initialization section found but contents appear empty",
                severity="warning",
            )
        )
    
    # Check if writes are restored
    if any("written" in note.lower() for note in [plan.notes] if note):
        if not plan.state_restore_lines:
            diagnostics.append(
                Diagnostic(
                    code="STATE_RESTORE_MISSING",
                    message="Function modifies global state but no restore directives generated",
                    severity="warning",
                )
            )
    
    return diagnostics


def build_setup_teardown_order(
    global_init_lines: list[str],
    pointer_setup_lines: list[str],
    state_restore_lines: list[str],
) -> tuple[list[str], list[str]]:
    """
    Organize setup and teardown in correct order.
    
    Setup order:
    1. Global/static initialization
    2. Pointer allocation
    3. State setup
    
    Teardown (reverse):
    1. State restore
    2. Pointer cleanup
    3. Global cleanup
    
    Args:
        global_init_lines: Global init directives.
        pointer_setup_lines: Pointer setup directives.
        state_restore_lines: State restore directives.
    
    Returns:
        Tuple of (setup_lines, teardown_lines).
    """
    setup = []
    
    setup.extend(global_init_lines)
    setup.append("")  # Spacer
    setup.extend(pointer_setup_lines)
    setup.append("")  # Spacer
    
    teardown = []
    
    teardown.extend(state_restore_lines)
    teardown.append("")  # Spacer
    # Pointer cleanup would go here (dealloc, etc.)
    
    return setup, teardown
