# backend/core/engine.py

from backend.core.lexer import tokenize
from backend.core.parser import Parser
from backend.core.solver import solve
from backend.core.constraints import apply_constraints


def solve_equation(expression: str, constraints=None):
    # 1. Lexer
    tokens = tokenize(expression)
    print("TOKENS:", tokens)  # debug

    # 2. Parser (FIXED)
    parser = Parser(tokens)
    parsed = parser.parse()

    print("PARSED OUTPUT:", parsed)  # debug
    print("TYPE:", type(parsed))  # debug

    # 🔥 SAFETY CHECK (IMPORTANT)
    if not isinstance(parsed, dict):
        raise Exception(f"Parser did not return valid equation: {parsed}")

    # 3. Solver
    solutions = solve(parsed)

    print("TOTAL SOLUTIONS:", len(solutions))

    for s in solutions[:10]:  # only first 10
        print(s)

    # 4. Constraints
    if constraints:
        solutions = apply_constraints(solutions, constraints)

    return solutions