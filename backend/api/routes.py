from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from core.constraints import apply_constraints
from core.lexer import tokenize
from core.normalizer import normalize
from core.parser import Parser
from core.solver import solve

router = APIRouter()


class SolveBody(BaseModel):
    equation: str
    constraints: List[str] = []


def _parser_tokens(raw_tokens):
    out = []
    for t in raw_tokens:
        name = t.type.name
        if name == "EQUAL":
            name = "EQUALS"
        if t.value is not None:
            out.append({"type": name, "value": t.value})
        else:
            out.append({"type": name})
    return out


@router.post("/solve")
def solve_equation(body: SolveBody):
    try:
        raw = tokenize(body.equation)
        tokens = _parser_tokens(raw)
        ast = Parser(tokens).parse()
        coeffs, const = normalize(ast)
        solutions = solve({"coefficients": coeffs, "target": const})
        final = apply_constraints(solutions, body.constraints)
        return {"solutions": final}
    except Exception as e:
        return {"error": str(e)}
