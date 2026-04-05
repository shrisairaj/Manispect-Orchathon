from core.constraints import apply_constraints
from core.lexer import tokenize
from core.parser import Parser
from core.solver import solve


def solve_equation(expression: str, constraints=None):
    if constraints is None:
        constraints = []

    tokens = tokenize(expression)
    print()
    print("Tokens:", tokens)
    parsed = Parser(tokens).parse()

    if not isinstance(parsed, dict):
        raise TypeError(f"Parser did not return a dict: {parsed!r}")

    solutions = solve(parsed)

    if constraints:
        solutions = apply_constraints(solutions, constraints)

    total = len(solutions)
    shown = solutions[:10]

    return {
        "total_solutions": total,
        "shown_solutions": len(shown),
        "solutions": shown,
    }
