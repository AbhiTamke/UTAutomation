"""
stub_profiles.py — Smart stub behavior definitions and selection.

Provides templates for stub function behavior and automated selection
based on function analysis and test intent.
"""

from __future__ import annotations

from vcast_automation.models.core import FunctionModel


def select_stub_profile(
    function_model: FunctionModel,
    test_family: str,
    overrides: dict | None,
) -> str:
    """
    Automatically select appropriate stub profile for a function.
    
    Profiles:
    - 'passthrough': stub returns input or minimal value
    - 'error': stub returns error code
    - 'side_effect': stub modifies parameters/globals
    - 'deterministic': stub returns fixed value
    - 'sequence': stub cycles through value list
    
    Args:
        function_model: Function being tested.
        test_family: Test case family (baseline, error, etc).
        overrides: Manual profile overrides.
    
    Returns:
        Selected profile name.
    """
    if overrides is None:
        overrides = {}
    
    # Check manual override first
    if function_model.function_name in overrides:
        return overrides[function_model.function_name].get("profile", "passthrough")
    
    # Heuristic selection based on function analysis
    
    # Error cases should use error stub
    if test_family in ("error", "negative"):
        return "error"
    
    # If function has side effects, use side_effect stub
    if function_model.globals_written or function_model.external_calls:
        return "side_effect"
    
    # If function returns value, use deterministic/passthrough
    if "void" not in function_model.return_type.lower():
        return "deterministic"
    
    # Default
    return "passthrough"


def build_stub_behavior(
    profile_name: str,
    context: dict,
) -> list[str]:
    """
    Generate stub behavior directives based on profile.
    
    Args:
        profile_name: Stub profile name.
        context: Context dict with keys:
            - function_name
            - return_type
            - parameters (list)
            - test_family
    
    Returns:
        List of VectorCAST stub directives.
    """
    lines = []
    fn_name = context.get("function_name", "stub_func")
    return_type = context.get("return_type", "void")
    
    if profile_name == "passthrough":
        lines.append(f"// Stub: {fn_name} passthrough")
        if "void" not in return_type.lower():
            lines.append(f"STUB_RETURN({fn_name}, 0)")
    
    elif profile_name == "error":
        lines.append(f"// Stub: {fn_name} error")
        lines.append(f"STUB_RETURN({fn_name}, -1)")
    
    elif profile_name == "deterministic":
        lines.append(f"// Stub: {fn_name} deterministic")
        lines.append(f"STUB_RETURN({fn_name}, 42)")
    
    elif profile_name == "side_effect":
        lines.append(f"// Stub: {fn_name} with side effects")
        lines.append(f"STUB_MODIFY_GLOBAL(some_global, 1)")
        if "void" not in return_type.lower():
            lines.append(f"STUB_RETURN({fn_name}, 0)")
    
    elif profile_name == "sequence":
        lines.append(f"// Stub: {fn_name} sequence")
        lines.append(f"STUB_SEQUENCE({fn_name}, [0, 1, -1, 999])")
    
    else:
        # Unknown profile, default to passthrough
        lines.append(f"// Stub: {fn_name} (unknown profile, using passthrough)")
        if "void" not in return_type.lower():
            lines.append(f"STUB_RETURN({fn_name}, 0)")
    
    return lines


def get_profile_description(profile_name: str) -> str:
    """Get human-readable description of a stub profile."""
    descriptions = {
        "passthrough": "Stub returns default/passthrough value without side effects",
        "error": "Stub simulates error condition (returns -1 or error code)",
        "side_effect": "Stub modifies globals or parameter state",
        "deterministic": "Stub returns fixed deterministic value",
        "sequence": "Stub cycles through a sequence of return values",
    }
    return descriptions.get(profile_name, "Unknown profile")


def list_available_profiles() -> list[str]:
    """Return list of available stub profile names."""
    return ["passthrough", "error", "deterministic", "side_effect", "sequence"]
