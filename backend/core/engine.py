# backend/core/engine.py

from backend.core.lexer import tokenize
from backend.core.parser import Parser
from backend.core.solver import solve
from backend.core.constraints import apply_constraints, compile_bounds


def solve_equation(expression: str, constraints=None):
    """
    Full pipeline:
    Input → Lexer → Parser → Solver → Constraints → Output
    """

    # -------------------
    # 1. Lexer
    # -------------------
    tokens = tokenize(expression)
    print("TOKENS:", tokens)

    # -------------------
    # 2. Parser
    # -------------------
    parser = Parser(tokens)
    parsed = parser.parse()

    print("PARSED OUTPUT:", parsed)
    print("TYPE:", type(parsed))

    # Safety check
    if not isinstance(parsed, dict):
        raise Exception(f"Parser did not return valid equation: {parsed}")

    # -------------------
    # 3. Solver
    # -------------------
    bounds = compile_bounds(constraints) if constraints else None
    all_solutions = solve(parsed, bounds=bounds)

    print("TOTAL SOLUTIONS:", len(all_solutions))

    # -------------------
    # 4. Apply constraints (Safety net)
    # -------------------
    # Most constraints are pre-handled by bounds in solve(), but we apply
    # them here to catch any variables not present in the equation.
    if constraints:
        all_solutions = apply_constraints(all_solutions, constraints)

    # -------------------
    # 5. Limit and sort output (IMPORTANT)
    # -------------------
    MAX_OUTPUT = 50
    import heapq
    if len(all_solutions) > MAX_OUTPUT:
        final_solutions = heapq.nsmallest(MAX_OUTPUT, all_solutions, key=lambda s: sum(s.values()))
    else:
        all_solutions.sort(key=lambda s: sum(s.values()))
        final_solutions = all_solutions

    # -------------------
    # 6. Return clean result
    # -------------------
    return {
        "total_solutions": len(all_solutions),
        "shown_solutions": len(final_solutions),
        "solutions": final_solutions
    }