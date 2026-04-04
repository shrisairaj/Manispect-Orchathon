from backend.core.lexer import tokenize

def run_test(expr):
    print(f"\nInput: {expr}")
    try:
        tokens = tokenize(expr)
        print("Output:", tokens)
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    run_test("10x + 20y = 100")
    run_test("(5a + 3b) * 2 = 50")
    run_test("x1 + y2 + z3 = 30")
    run_test("100 = 50x + 50y")
    run_test("10apple + 20banana = 200")