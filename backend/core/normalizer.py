from collections import defaultdict

from core.tree import BinaryOp, Equation, Number, Variable


def _affine(node):
    if isinstance(node, Number):
        return {}, node.value
    if isinstance(node, Variable):
        return {node.name: 1}, 0
    if isinstance(node, BinaryOp):
        if node.op == "PLUS":
            lc, lconst = _affine(node.left)
            rc, rconst = _affine(node.right)
            coeffs = defaultdict(int, lc)
            for k, v in rc.items():
                coeffs[k] += v
            return dict(coeffs), lconst + rconst
        if node.op == "MINUS":
            lc, lconst = _affine(node.left)
            rc, rconst = _affine(node.right)
            coeffs = defaultdict(int, lc)
            for k, v in rc.items():
                coeffs[k] -= v
            return dict(coeffs), lconst - rconst
        if node.op == "MUL":
            left, right = node.left, node.right
            if isinstance(left, Number) and isinstance(right, Variable):
                return {right.name: left.value}, 0
            if isinstance(right, Number) and isinstance(left, Variable):
                return {left.name: right.value}, 0
        raise ValueError("Non-linear expression")
    raise ValueError("Unsupported AST node")


def normalize(ast):
    if not isinstance(ast, Equation):
        raise ValueError("Expected an equation")
    lc, lconst = _affine(ast.left)
    rc, rconst = _affine(ast.right)
    coeffs = defaultdict(int, lc)
    for k, v in rc.items():
        coeffs[k] -= v
    const = rconst - lconst
    return dict(coeffs), const
