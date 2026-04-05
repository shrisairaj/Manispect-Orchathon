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
        left_coeffs, left_const = self.eval_poly(eq.left)
        right_coeffs, right_const = self.eval_poly(eq.right)

        # Move all variables to left, all constants to right
        coeffs = {}
        for k, v in left_coeffs.items():
            coeffs[k] = coeffs.get(k, 0) + v
        for k, v in right_coeffs.items():
            coeffs[k] = coeffs.get(k, 0) - v

        target = right_const - left_const

        return {
            "coefficients": coeffs,
            "target": target
        }

    def eval_poly(self, node):
        if isinstance(node, Number):
            return {}, node.value

        if isinstance(node, Variable):
            return {node.name: 1}, 0

        if isinstance(node, BinaryOp):
            l_coeffs, l_const = self.eval_poly(node.left)
            r_coeffs, r_const = self.eval_poly(node.right)

            if node.op == TokenType.PLUS:
                c = dict(l_coeffs)
                for k, v in r_coeffs.items():
                    c[k] = c.get(k, 0) + v
                return c, l_const + r_const

            if node.op == TokenType.MINUS:
                c = dict(l_coeffs)
                for k, v in r_coeffs.items():
                    c[k] = c.get(k, 0) - v
                return c, l_const - r_const

            if node.op == TokenType.MUL:
                if l_coeffs and r_coeffs:
                    raise Exception("Non-linear equations (variable * variable) are not supported.")

                c = {}
                if l_coeffs:  # left has variables, so multiply them by right constant
                    for k, v in l_coeffs.items():
                        c[k] = v * r_const
                    return c, l_const * r_const
                else:  # right has variables, so multiply them by left constant
                    for k, v in r_coeffs.items():
                        c[k] = v * l_const
                    return c, l_const * r_const

            if node.op == TokenType.DIV:
                if r_coeffs:
                    raise Exception("Dividing by a variable in the equation is not supported.")
                if r_const == 0:
                    raise Exception("Division by zero.")

                c = {}
                for k, v in l_coeffs.items():
                    if v % r_const != 0:
                        raise Exception("Fractional coefficients are not supported.")
                    c[k] = v // r_const
                if l_const % r_const != 0:
                    raise Exception("Fractional constants are not supported.")
                return c, l_const // r_const

        raise Exception(f"Unrecognized node in expression: {type(node)}")