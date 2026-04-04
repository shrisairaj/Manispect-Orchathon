from backend.core.solver import solve

# Mock parser output
equation = {
    "coefficients": {
        "x": 100,
        "y": 250
    },
    "target": 10000
}

solutions = solve(equation)

print("Solutions:")
for s in solutions:
    print(s)