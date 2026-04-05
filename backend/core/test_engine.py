from core.engine import solve_equation

expr = "10a + 5b = 20"
constraints = ["a>=0"]

result = solve_equation(expr, constraints)

print("\nFINAL RESULT:\n")

print("Total Solutions:", result["total_solutions"])
print("Shown Solutions:", result["shown_solutions"])

print("\nSolutions:")
for sol in result["solutions"]:
    print(sol)