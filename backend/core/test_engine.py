from core.engine import solve_equation

expr = "10a+15b+20c+50d+5e=1000"
constraints = ["a>=999"]

result = solve_equation(expr, constraints)

print("\nFINAL RESULT:")
for r in result:
    print(r)