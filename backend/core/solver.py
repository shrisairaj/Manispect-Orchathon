# backend/core/solver.py

# Optimized solver for linear Diophantine equations:
# a1*x1 + a2*x2 + ... + an*xn = target
# where all xi >= 0 (whole units)

def solve(equation):
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
        return _solve_one_var(coeffs, variables, target)

    if len(variables) == 2:
        return _solve_two_var(coeffs, variables, target)

    return _solve_multi_var(coeffs, variables, target)


# -------------------------------
# 1 Variable (O(1))
# -------------------------------
def _solve_one_var(coeffs, variables, target):
    var = variables[0]
    coeff = coeffs[var]

    if target % coeff != 0:
        return []

    value = target // coeff
    if value < 0:
        return []

    return [{var: value}]


# -------------------------------
# 2 Variables (O(n))
# -------------------------------
def _solve_two_var(coeffs, variables, target):
    v1, v2 = variables
    a = coeffs[v1]
    b = coeffs[v2]

    solutions = []
    append = solutions.append

    # iterate smaller range
    max_v1 = target // a

    for x in range(max_v1 + 1):
        remaining = target - a * x

        if remaining % b == 0:
            y = remaining // b
            if y >= 0:
                append({v1: x, v2: y})

    return solutions


# -------------------------------
# Multi-variable (Backtracking optimized)
# -------------------------------
def _solve_multi_var(coeffs, variables, target):
    solutions = []
    append = solutions.append

    n = len(variables)

    def backtrack(index, current, remaining):
        # Last variable → compute directly
        if index == n - 1:
            var = variables[index]
            coeff = coeffs[var]

            if remaining % coeff == 0:
                val = remaining // coeff
                if val >= 0:
                    current[var] = val
                    append(current.copy())
            return

        var = variables[index]
        coeff = coeffs[var]

        # Max possible value for this variable
        max_val = remaining // coeff

        for value in range(max_val + 1):
            new_remaining = remaining - coeff * value

            # Early pruning
            if new_remaining < 0:
                break

            current[var] = value
            backtrack(index + 1, current, new_remaining)

    backtrack(0, {}, target)
    return solutions