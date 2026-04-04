from core.parser import Parser
tokens = [
    {"type": "NUMBER", "value": 10},
    {"type": "MUL"},
    {"type": "VARIABLE", "value": "x"},
    {"type": "PLUS"},
    {"type": "NUMBER", "value": 20},
    {"type": "MUL"},
    {"type": "VARIABLE", "value": "y"},
    {"type": "EQUALS"},
    {"type": "NUMBER", "value": 100},
]

parser = Parser(tokens)
ast = parser.parse()

print(ast)
print(ast.left)
print(ast.right)