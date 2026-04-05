from core.engine import solve_equation

expr = "10a+15b+20c+50d+5e=1000"
constraints = ["a>=2"]

result = solve_equation(expr, constraints)

print("\nFINAL RESULT:\n")

print("Total Solutions:", result["total_solutions"])
print("Shown Solutions:", result["shown_solutions"])

print("\nSolutions:")
for sol in result["solutions"]:
    print(sol)