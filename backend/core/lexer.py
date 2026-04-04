# backend/core/lexer.py

from enum import Enum


class TokenType(Enum):
    NUMBER = 1
    VARIABLE = 2
    PLUS = 3
    MINUS = 4
    MUL = 5
    DIV = 6
    EQUAL = 7
    LPAREN = 8
    RPAREN = 9


class Token:
    __slots__ = ("type", "value")

    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type.name}:{self.value}" if self.value is not None else f"{self.type.name}"


# Fast O(1) operator lookup
_OPERATOR_MAP = {
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.MUL,
    "/": TokenType.DIV,
    "=": TokenType.EQUAL,
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
}


def tokenize(expression: str):
    tokens = []
    append = tokens.append  # local binding for speed

    i = 0
    n = len(expression)

    while i < n:
        char = expression[i]

        # Skip whitespace (fast path)
        if char <= " ":
            i += 1
            continue

        # NUMBER (multi-digit, optimized slicing)
        if "0" <= char <= "9":
            start = i
            i += 1
            while i < n and "0" <= expression[i] <= "9":
                i += 1
            append(Token(TokenType.NUMBER, int(expression[start:i])))
            continue

        # VARIABLE (multi-letter + digits allowed after first char)
        if ("a" <= char <= "z") or ("A" <= char <= "Z"):
            start = i
            i += 1

            while i < n:
                c = expression[i]
                if ("a" <= c <= "z") or ("A" <= c <= "Z") or ("0" <= c <= "9"):
                    i += 1
                else:
                    break

            append(Token(TokenType.VARIABLE, expression[start:i]))
            continue

        # OPERATOR / SYMBOL
        token_type = _OPERATOR_MAP.get(char)
        if token_type:
            append(Token(token_type))
            i += 1
            continue

        # ERROR handling (clear + useful)
        raise ValueError(f"Invalid character '{char}' at position {i}")

    return tokens