from backend.core.constraints import apply_constraints

solutions = [
    {"x": 10, "y": 0},
    {"x": 8, "y": 1},
    {"x": 6, "y": 2},
]

constraints = ["x >= 8", "y <= 1"]

print(apply_constraints(solutions, constraints))