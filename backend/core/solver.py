# backend/core/solver.py

# Optimized solver for linear Diophantine equations:
# a1*x1 + a2*x2 + ... + an*xn = target
# where all xi >= 0 (whole units)
from math import gcd
from functools import reduce


def is_valid(coeffs, target):
    g = reduce(gcd, coeffs.values())
    return target % g == 0


def solve(equation, bounds=None):
    """
    Main entry point.
    Expects:
    {
        "coefficients": {"x": 10, "y": 20, ...},
        "target": 100
    }
    """
    coeffs = equation["coefficients"]
    target = equation["target"]

    # 🔥 ADD THIS CHECK HERE
    if not is_valid(coeffs, target):
        return []

    # Basic validation
    if target < 0:
        return []

    # Remove zero coefficients (avoid division issues)
    coeffs = {k: v for k, v in coeffs.items() if v != 0}

    if not coeffs:
        return []

    variables = list(coeffs.keys())

    # Sort variables by descending coefficient (optimization → reduces search space)
    variables.sort(key=lambda v: -coeffs[v])

    # Choose optimized path
    if len(variables) == 1:
        return _solve_one_var(coeffs, variables, target, bounds)

    if len(variables) == 2:
        return _solve_two_var(coeffs, variables, target, bounds)

    return _solve_multi_var(coeffs, variables, target, bounds)


# -------------------------------
# 1 Variable (O(1))
# -------------------------------
def _solve_one_var(coeffs, variables, target, bounds):
    var = variables[0]
    coeff = coeffs[var]

    if target % coeff != 0:
        return []

    value = target // coeff
    if value < 0:
        return []

    if bounds:
        bv = bounds.get(var, {})
        if value < bv.get("min", 0) or value > bv.get("max", float('inf')) or value in bv.get("exclude", set()):
            return []

    return [{var: value}]


# -------------------------------
# 2 Variables (O(n))
# -------------------------------
def _solve_two_var(coeffs, variables, target, bounds):
    v1, v2 = variables
    a = coeffs[v1]
    b = coeffs[v2]

    solutions = []
    append = solutions.append

    # iterate smaller range
    max_v1 = target // a

    min_x = 0
    max_x = max_v1
    min_y = 0
    max_y = float('inf')
    ex_x = set()
    ex_y = set()

    if bounds:
        bx = bounds.get(v1, {})
        min_x = max(0, bx.get("min", 0))
        max_x = min(max_v1, bx.get("max", float('inf')))
        ex_x = bx.get("exclude", set())

        by = bounds.get(v2, {})
        min_y = max(0, by.get("min", 0))
        max_y = by.get("max", float('inf'))
        ex_y = by.get("exclude", set())

    for x in range(min_x, int(max_x) + 1):
        if x in ex_x:
            continue

        remaining = target - a * x

        if remaining % b == 0:
            y = remaining // b
            if y >= min_y and y <= max_y and y not in ex_y:
                append({v1: x, v2: y})

    return solutions


# -------------------------------
# Multi-variable (Backtracking optimized)
# -------------------------------
def _solve_multi_var(coeffs, variables, target, bounds):
    MAX_SOLUTIONS = 1000
    solutions = []
    append = solutions.append

    n = len(variables)

    def backtrack(index, current, remaining):
        # Last variable → compute directly
        if len(solutions) >= MAX_SOLUTIONS:
            return

        if index == n - 1:
            var = variables[index]
            coeff = coeffs[var]

            min_v = 0
            max_v = float('inf')
            ex_v = set()
            if bounds:
                bv = bounds.get(var, {})
                min_v = max(0, bv.get("min", 0))
                max_v = bv.get("max", float('inf'))
                ex_v = bv.get("exclude", set())

            if remaining % coeff == 0:
                val = remaining // coeff
                if val >= min_v and val <= max_v and val not in ex_v:
                    current[var] = val
                    append(current.copy())
            return

        var = variables[index]
        coeff = coeffs[var]

        # Max possible value for this variable
        max_val = remaining // coeff

        min_v = 0
        max_v = max_val
        ex_v = set()

        if bounds:
            bv = bounds.get(var, {})
            min_v = max(0, bv.get("min", 0))
            max_v = min(max_val, bv.get("max", float('inf')))
            ex_v = bv.get("exclude", set())

        for value in range(min_v, int(max_v) + 1):
            if value in ex_v:
                continue

            new_remaining = remaining - coeff * value

            # Early pruning
            if new_remaining < 0:
                break

            current[var] = value
            backtrack(index + 1, current, new_remaining)

    backtrack(0, {}, target)
    return solutions