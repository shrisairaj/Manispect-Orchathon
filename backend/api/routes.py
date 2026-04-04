from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from core.constraints import apply_constraints
from core.lexer import tokenize
from core.parser import Parser
from core.solver import solve

router = APIRouter()


class SolveBody(BaseModel):
    equation: str
    constraints: List[str] = []


@router.post("/solve")
def solve_equation(body: SolveBody):
    try:
        tokens = tokenize(body.equation)
        parsed = Parser(tokens).parse()
        solutions = solve(parsed)
        final = apply_constraints(solutions, body.constraints)
        return {"solutions": final}
    except Exception as e:
        return {"error": str(e)}
