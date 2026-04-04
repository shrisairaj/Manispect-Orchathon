from core.lexer import TokenType
from core.tree import BinaryOp, Equation, Number, Variable


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

        if token_type and token.type != token_type:
            raise Exception(f"Expected {token_type}, got {token.type}")

        self.pos += 1
        return token

    def parse(self):
        left = self.expr()

        # 🔥 FIX: make sure '=' is detected correctly
        if self.current() and self.current().type == TokenType.EQUAL:
            self.eat(TokenType.EQUAL)
            right = self.expr()
            eq = Equation(left, right)

            # convert to solver format
            return self.build_equation(eq)

        # ❌ NEVER return raw AST here
        raise Exception("Invalid equation format. '=' missing or not parsed correctly")

    def expr(self):
        node = self.term()

        while self.current() and self.current().type in (TokenType.PLUS, TokenType.MINUS):
            op = self.eat().type
            right = self.term()
            node = BinaryOp(node, op, right)

        return node

    def term(self):
        node = self.factor()

        while True:
            curr = self.current()

            # explicit * or /
            if curr and curr.type in (TokenType.MUL, TokenType.DIV):
                op = self.eat().type
                right = self.factor()
                node = BinaryOp(node, op, right)

            # 🔥 implicit multiplication (IMPORTANT FIX)
            elif curr and curr.type in (TokenType.NUMBER, TokenType.VARIABLE, TokenType.LPAREN):
                # treat as multiplication
                right = self.factor()
                node = BinaryOp(node, TokenType.MUL, right)

            else:
                break

        return node

    def factor(self):
        token = self.current()

        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Number(token.value)

        if token.type == TokenType.VARIABLE:
            self.eat(TokenType.VARIABLE)
            return Variable(token.value)

        if token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node

        raise Exception(f"Unexpected token: {token}")

    # -------------------------
    # 🔥 IMPORTANT PART
    # Convert AST → coefficients
    # -------------------------
    def build_equation(self, eq):
        coeffs = {}
        target = self.evaluate(eq.right)

        self.extract_terms(eq.left, coeffs)

        return {
            "coefficients": coeffs,
            "target": target
        }

    def extract_terms(self, node, coeffs):
        # Case 1: Addition
        if isinstance(node, BinaryOp) and node.op == TokenType.PLUS:
            self.extract_terms(node.left, coeffs)
            self.extract_terms(node.right, coeffs)

        # Case 2: Subtraction
        elif isinstance(node, BinaryOp) and node.op == TokenType.MINUS:
            self.extract_terms(node.left, coeffs)

            temp = {}
            self.extract_terms(node.right, temp)

            for k, v in temp.items():
                coeffs[k] = coeffs.get(k, 0) - v

        # Case 3: Multiplication (MOST IMPORTANT)
        elif isinstance(node, BinaryOp) and node.op == TokenType.MUL:

            # number * variable
            if isinstance(node.left, Number) and isinstance(node.right, Variable):
                coeffs[node.right.name] = coeffs.get(node.right.name, 0) + node.left.value

            # variable * number
            elif isinstance(node.right, Number) and isinstance(node.left, Variable):
                coeffs[node.left.name] = coeffs.get(node.left.name, 0) + node.right.value

        # Case 4: Single variable (like x → 1x)
        elif isinstance(node, Variable):
            coeffs[node.name] = coeffs.get(node.name, 0) + 1

    def evaluate(self, node):
        if isinstance(node, Number):
            return node.value

        if isinstance(node, BinaryOp):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)

            if node.op == TokenType.PLUS:
                return left + right
            if node.op == TokenType.MINUS:
                return left - right
            if node.op == TokenType.MUL:
                return left * right
            if node.op == TokenType.DIV:
                return left // right

        raise Exception("Invalid expression")