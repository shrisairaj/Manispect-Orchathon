# backend/core/engine.py

from backend.core.lexer import tokenize
from backend.core.parser import parse   # your friend's module
from backend.core.solver import solve
from backend.core.constraints import apply_constraints


def solve_equation(expression: str, constraints=None):
    """
    Full pipeline:
    string → tokens → parsed → solved → filtered
    """

    # 1. Lexer
    tokens = tokenize(expression)

    # 2. Parser
    parsed = parse(tokens)

    # Expected format:
    # {
    #     "coefficients": {"x": 10, "y": 20},
    #     "target": 100
    # }

    # 3. Solver
    solutions = solve(parsed)

    # 4. Constraints (optional)
    if constraints:
        solutions = apply_constraints(solutions, constraints)

    return solutions