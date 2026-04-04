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