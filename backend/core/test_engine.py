from backend.core.engine import solve_equation

expr = "50x"
constraints = ["x=10"]

result = solve_equation(expr, constraints)

print("\nFINAL RESULT:\n")

print("Total Solutions:", result["total_solutions"])
print("Shown Solutions:", result["shown_solutions"])

print("\nSolutions:")
for sol in result["solutions"]:
    print(sol)