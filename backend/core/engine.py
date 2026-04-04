from core.constraints import apply_constraints
from core.lexer import tokenize
from core.parser import Parser
from core.solver import solve


def solve_equation(expression: str, constraints=None):
    if constraints is None:
        constraints = []
    tokens = tokenize(expression)
    parsed = Parser(tokens).parse()
    solutions = solve(parsed)
    if constraints:
        solutions = apply_constraints(solutions, constraints)
    return solutions
