from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from backend.core.engine import solve_equation

router = APIRouter()

class SolveRequest(BaseModel):
    expression: str
    constraints: Optional[List[str]] = None

@router.post("/solve")
def solve_endpoint(request: SolveRequest):
    try:
        # solve_equation() only takes 1 to 2 positional arguments:
        # expression: str, constraints: list = None
        result = solve_equation(request.expression, request.constraints)
        return result
    except Exception as e:
        return {"error": str(e)}