from core.tree import Number, Variable, BinaryOp, Equation

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def eat(self, token_type=None):
        token = self.current()
        if token is None:
            return None

        if token_type and token["type"] != token_type:
            raise Exception(f"Expected {token_type}, got {token['type']}")

        self.pos += 1
        return token

    def parse(self):
        left = self.expr()
        if self.current() and self.current()["type"] == "EQUALS":
            self.eat("EQUALS")
            right = self.expr()
            return Equation(left, right)
        return left

    def expr(self):
        node = self.term()

        while self.current() and self.current()["type"] in ("PLUS", "MINUS"):
            op = self.eat()["type"]
            right = self.term()
            node = BinaryOp(node, op, right)

        return node

    def term(self):
        node = self.factor()

        while self.current() and self.current()["type"] in ("MUL", "DIV"):
            op = self.eat()["type"]
            right = self.factor()
            node = BinaryOp(node, op, right)

        return node

    def factor(self):
        token = self.current()

        if token["type"] == "NUMBER":
            self.eat("NUMBER")
            return Number(token["value"])

        if token["type"] == "VARIABLE":
            self.eat("VARIABLE")
            return Variable(token["value"])

        if token["type"] == "LPAREN":
            self.eat("LPAREN")
            node = self.expr()
            self.eat("RPAREN")
            return node

        raise Exception(f"Unexpected token: {token}")