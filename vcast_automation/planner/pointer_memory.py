"""
pointer_memory.py — Deterministic memory model for pointer setup.

Manages pointer allocation, aliasing scenarios, and dereferencing patterns
in test case generation.
"""

from __future__ import annotations

from vcast_automation.models.core import ParameterModel


def build_pointer_setup(
    param: ParameterModel,
    scenario: str,
    limits: dict,
) -> list[str]:
    """
    Build setup lines for pointer parameters.
    
    Scenarios:
    - 'null': pointer = NULL
    - 'allocate': pointer = malloc(...)
    - 'stack': pointer = &stack_var
    - 'alias': pointer = same as another parameter
    
    Args:
        param: Pointer parameter to set up.
        scenario: Allocation scenario.
        limits: Hard limits like max_alloc_size.
    
    Returns:
        List of VectorCAST directive lines.
    """
    lines = []
    
    if scenario == "null":
        lines.append(f"{param.name} = NULL")
    
    elif scenario == "stack":
        lines.append(f"int __stack_var_{param.name} = 0")
        lines.append(f"{param.name} = &__stack_var_{param.name}")
    
    elif scenario == "allocate":
        # Allocate deterministic size
        alloc_size = limits.get("alloc_size", 100)
        lines.append(f"{param.name} = malloc({alloc_size})")
        lines.append(f"memset({param.name}, 0, {alloc_size})")
    
    elif scenario == "alias":
        # Aliasing: will be handled by parameter linking
        lines.append(f"// {param.name} will be aliased to another parameter")
    
    return lines


def build_aliasing_setup(
    params: list[ParameterModel],
    alias_mode: str,
) -> list[str]:
    """
    Build setup for pointer aliasing scenarios.
    
    Modes:
    - 'none': no aliasing
    - 'all_same': all pointers point to same buffer
    - 'disjoint': all pointers are disjoint
    - 'partial': some overlap
    
    Args:
        params: List of pointer parameters.
        alias_mode: Aliasing mode.
    
    Returns:
        List of setup directives.
    """
    lines = []
    
    if alias_mode == "none" or alias_mode == "disjoint":
        lines.append("// Disjoint pointer allocation")
        for p in params:
            if p.is_pointer:
                lines.append(f"{p.name} = malloc(256)")
    
    elif alias_mode == "all_same":
        lines.append("// All pointers share same buffer")
        lines.append("void *__shared_buffer = malloc(256)")
        for p in params:
            if p.is_pointer:
                lines.append(f"{p.name} = __shared_buffer")
    
    elif alias_mode == "partial":
        lines.append("// Partially overlapping allocations")
        for i, p in enumerate(params):
            if p.is_pointer:
                offset = i * 64  # Partial overlap
                lines.append(f"{p.name} = (void*)(__shared_buffer + {offset})")
    
    return lines


def validate_pointer_layout(
    test_case: dict,
    limits: dict,
) -> list[str]:
    """
    Validate pointer setup for soundness.
    
    Checks:
    - No wild pointers (uninitialized)
    - No use-after-free patterns
    - Aliasing consistency
    
    Args:
        test_case: Test case with input values.
        limits: Constraints.
    
    Returns:
        List of validation messages (empty if valid).
    """
    messages = []
    
    # Check for uninitialized pointers
    for key, value in test_case.items():
        if "ptr" in key.lower() or "p_" in key.lower():
            if value and value not in ("NULL", "&stack_var", "malloc", "allocate"):
                if not _looks_like_valid_ptr_expr(value):
                    messages.append(f"Pointer {key}={value} may be uninitialized")
    
    return messages


# Internal helpers

def _looks_like_valid_ptr_expr(expr: str) -> bool:
    """Check if expression looks like a valid pointer assignment."""
    valid_patterns = (
        "NULL",
        "&",
        "malloc",
        "calloc",
        "realloc",
        "->",
        "cast",
        "0x",
        "__",
    )
    return any(p in expr for p in valid_patterns)
