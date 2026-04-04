class Number:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


class Variable:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class BinaryOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"({self.left} {self.op} {self.right})"


class Equation:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.left} = {self.right}"