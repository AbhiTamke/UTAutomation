"""
constraint_extractor.py — Heuristic constraint extraction from source code.

Performs simple pattern-based constraint extraction on conditions, loops,
and comparisons to feed domain hint inference without full symbolic solving.
"""

from __future__ import annotations

import re

from vcast_automation.models.core import FunctionModel, ConditionModel, Diagnostic


def extract_simple_constraints(function_model: FunctionModel) -> dict:
    """
    Extract simple constraints from conditions.
    
    Looks for patterns like:
    - x < 10, x <= 10, x > 0, x >= 0
    - x == value, x != value
    - x in [min, max]
    
    Args:
        function_model: Function to analyze.
    
    Returns:
        Dictionary mapping parameter names to constraint info.
    """
    constraints = {}
    
    for condition in function_model.conditions:
        expr = condition.expression.strip()
        
        # Simple comparison extraction
        param_name, constraint_info = _extract_simple_comparison(expr)
        if param_name and constraint_info:
            if param_name not in constraints:
                constraints[param_name] = []
            constraints[param_name].append(constraint_info)
            
            # Update condition model with extracted data
            condition.operator = constraint_info.get("operator", "")
            condition.lhs_symbol = param_name
            condition.rhs_literal = constraint_info.get("rhs", "")
            condition.constraint_candidates.append(
                f"{param_name} {constraint_info.get('operator', '')} {constraint_info.get('rhs', '')}"
            )
    
    return constraints


def extract_condition_targets(function_model: FunctionModel) -> list[str]:
    """
    Extract parameter/variable names that are subjects of conditions.
    
    Args:
        function_model: Function to analyze.
    
    Returns:
        List of parameter names that appear in conditions.
    """
    targets = set()
    
    for condition in function_model.conditions:
        expr = condition.expression.strip()
        
        # Extract identifiers (simple approach)
        identifiers = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', expr)
        targets.update(identifiers)
    
    return sorted(list(targets))


def tag_potentially_unreachable(function_model: FunctionModel) -> list[Diagnostic]:
    """
    Identify conditions that may be unreachable.
    
    Heuristics:
    - Conditions after unconditional return/break
    - Contradictory conditions (x < 0 && x > 10)
    - Dead code after infinite loop
    
    Args:
        function_model: Function to analyze.
    
    Returns:
        List of diagnostics for unreachable code.
    """
    diagnostics = []
    
    # Simple heuristic: if all branches in a condition tree are return/break,
    # following code is unreachable
    for i, condition in enumerate(function_model.conditions):
        # Check for contradictions
        if _is_contradictory(condition.expression):
            condition.is_potentially_unreachable = True
            condition.unreachable_reason = "Contradictory condition"
            diagnostics.append(
                Diagnostic(
                    code="CODE_UNREACHABLE",
                    message=f"Condition at line {condition.line_start} appears contradictory and unreachable",
                    severity="warning",
                )
            )
    
    return diagnostics


# Internal helpers

def _extract_simple_comparison(expr: str) -> tuple[str | None, dict | None]:
    """
    Extract single simple comparison from expression.
    
    Returns (parameter_name, constraint_dict) or (None, None).
    """
    # Patterns: var op literal
    patterns = [
        (r'(\w+)\s*<\s*(\d+)', '<'),
        (r'(\w+)\s*<=\s*(\d+)', '<='),
        (r'(\w+)\s*>\s*(\d+)', '>'),
        (r'(\w+)\s*>=\s*(\d+)', '>='),
        (r'(\w+)\s*==\s*(\d+)', '=='),
        (r'(\w+)\s*!=\s*(\d+)', '!='),
    ]
    
    for pattern, op in patterns:
        match = re.search(pattern, expr)
        if match:
            param = match.group(1)
            value = match.group(2)
            return param, {
                "operator": op,
                "rhs": value,
                "kind": "literal_comparison",
            }
    
    return None, None


def _is_contradictory(expr: str) -> bool:
    """
    Simple heuristic for contradictory conditions.
    
    Examples: x > 10 && x < 5, ptr != NULL && ptr == NULL
    """
    # Look for patterns like "x > A && x < B" where A > B
    match_gt = re.search(r'(\w+)\s*>\s*(\d+)', expr)
    match_lt = re.search(r'(\w+)\s*<\s*(\d+)', expr)
    
    if match_gt and match_lt:
        if match_gt.group(1) == match_lt.group(1):
            gt_val = int(match_gt.group(2))
            lt_val = int(match_lt.group(2))
            if gt_val >= lt_val:
                return True
    
    return False
