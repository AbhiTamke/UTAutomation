"""
pairwise_engine.py — Pairwise strength reduction for combinatorial test reduction.

Implements pairwise/n-wise reduction to minimize test count while maintaining
parameter interaction coverage.
"""

from __future__ import annotations

import itertools
from collections import defaultdict


def build_pairwise_cases(
    param_value_map: dict[str, list[str]],
    hard_caps: dict,
) -> list[dict[str, str]]:
    """
    Generate pairwise test cases from parameter value assignments.
    
    Each pair of parameters should appear together in at least one test case.
    
    Args:
        param_value_map: {param_name: [value1, value2, ...]}
        hard_caps: {max_cases: N, ...}
    
    Returns:
        List of test case dictionaries with reduced count.
    """
    if not param_value_map:
        return []
    
    # Generate all possible combinations
    param_names = list(param_value_map.keys())
    
    if len(param_names) == 1:
        # Single parameter: one test per value
        param = param_names[0]
        return [{param: v} for v in param_value_map[param]]
    
    # Pairwise greedy algorithm: start with all combinations, then reduce
    all_combos = _generate_all_combinations(param_value_map)
    
    max_cases = hard_caps.get("max_cases", len(all_combos))
    
    if len(all_combos) <= max_cases:
        return all_combos
    
    # Greedy pairwise reduction: pick cases that cover most uncovered pairs
    selected = []
    uncovered_pairs = _init_uncovered_pairs(param_value_map)
    
    while uncovered_pairs and len(selected) < max_cases:
        # Pick the combination that covers the most uncovered pairs
        best_combo = None
        best_new_pairs = 0
        
        for combo in all_combos:
            if combo in selected:
                continue
            
            new_pairs = sum(
                1 for pair in uncovered_pairs
                if _combo_covers_pair(combo, pair)
            )
            
            if new_pairs > best_new_pairs:
                best_new_pairs = new_pairs
                best_combo = combo
        
        if best_combo is None:
            break
        
        selected.append(best_combo)
        
        # Mark covered pairs as covered
        uncovered_pairs = [
            pair for pair in uncovered_pairs
            if not _combo_covers_pair(best_combo, pair)
        ]
    
    return selected


def prioritize_cases(cases: list[dict[str, str]]) -> list[dict[str, str]]:
    """
    Prioritize test cases by execution impact.
    
    Places baseline/core cases first, negative cases later.
    
    Args:
        cases: List of test case dictionaries.
    
    Returns:
        Prioritized list.
    """
    # Simple prioritization: group by estimated complexity
    core_cases = []
    complex_cases = []
    
    for case in cases:
        # Heuristic: NULL/negative values = more complex
        has_special = any(
            v in ("NULL", "NAN", "INFINITY", "-INFINITY")
            for v in case.values()
        )
        
        if has_special:
            complex_cases.append(case)
        else:
            core_cases.append(case)
    
    return core_cases + complex_cases


# Internal helpers

def _generate_all_combinations(param_value_map: dict[str, list[str]]) -> list[dict[str, str]]:
    """Generate all possible combinations of parameter values."""
    param_names = list(param_value_map.keys())
    value_lists = [param_value_map[name] for name in param_names]
    
    combinations = []
    for value_combo in itertools.product(*value_lists):
        combo = {param_names[i]: value_combo[i] for i in range(len(param_names))}
        combinations.append(combo)
    
    return combinations


def _init_uncovered_pairs(param_value_map: dict[str, list[str]]) -> list[tuple]:
    """Initialize list of all parameter value pairs to cover."""
    param_names = list(param_value_map.keys())
    pairs = []
    
    for i in range(len(param_names)):
        for j in range(i + 1, len(param_names)):
            param_i, param_j = param_names[i], param_names[j]
            for v_i in param_value_map[param_i]:
                for v_j in param_value_map[param_j]:
                    pairs.append((param_i, v_i, param_j, v_j))
    
    return pairs


def _combo_covers_pair(combo: dict[str, str], pair: tuple) -> bool:
    """Check if a combination covers a specific pair."""
    param_i, v_i, param_j, v_j = pair
    return combo.get(param_i) == v_i and combo.get(param_j) == v_j
