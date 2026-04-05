# backend/core/constraints.py

import operator

# Supported operators
_OPS = {
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
    "==": operator.eq,
    "!=": operator.ne,
}


def parse_constraint(constraint_str):
    # Order matters (>= before >)
    for op in ["<=", ">=", "==", "!=", "<", ">"]:
        if op in constraint_str:
            left, right = constraint_str.split(op)
            var = left.strip()
            value = int(right.strip())
            return var, _OPS[op], value

    raise ValueError(f"Invalid constraint: {constraint_str}")


def apply_constraints(solutions, constraints):
    if not constraints:
        return solutions

    parsed = [parse_constraint(c) for c in constraints]

    filtered = []
    append = filtered.append

    for sol in solutions:
        valid = True

        for var, op_func, val in parsed:
            if var not in sol or not op_func(sol[var], val):
                valid = False
                break

        if valid:
            append(sol)

    return filtered


def compile_bounds(constraints):
    bounds = {}
    if not constraints:
        return bounds

    parsed = [parse_constraint(c) for c in constraints]
    for var, op_func, val in parsed:
        if var not in bounds:
            bounds[var] = {"min": 0, "max": float('inf'), "exclude": set()}

        if op_func == operator.ge:  # var >= val
            bounds[var]["min"] = max(bounds[var]["min"], val)
        elif op_func == operator.gt:  # var > val
            bounds[var]["min"] = max(bounds[var]["min"], val + 1)
        elif op_func == operator.le:  # var <= val
            bounds[var]["max"] = min(bounds[var]["max"], val)
        elif op_func == operator.lt:  # var < val
            bounds[var]["max"] = min(bounds[var]["max"], val - 1)
        elif op_func == operator.eq:  # var == val
            bounds[var]["min"] = max(bounds[var]["min"], val)
            bounds[var]["max"] = min(bounds[var]["max"], val)
        elif op_func == operator.ne:  # var != val
            bounds[var]["exclude"].add(val)

    return bounds