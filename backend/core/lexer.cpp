#include "lexer.h"
#include <cctype>
#include <stdexcept>

namespace quant {

Lexer::Lexer(std::string input)
    : input_(std::move(input)), position_(0) {}

char Lexer::peek() const {
    return position_ < input_.size() ? input_[position_] : '\0';
}

char Lexer::consume() {
    return position_ < input_.size() ? input_[position_++] : '\0';
}

void Lexer::skipWhitespace() {
    while (std::isspace(static_cast<unsigned char>(peek()))) {
        consume();
    }
}

Token Lexer::nextToken() {
    skipWhitespace();
    char current = peek();
    if (current == '\0') {
        return Token(TokenType::End, "", 0);
    }

    if (std::isdigit(static_cast<unsigned char>(current))) {
        size_t start = position_;
        long long value = 0;
        while (std::isdigit(static_cast<unsigned char>(peek()))) {
            value = value * 10 + (consume() - '0');
        }
        return Token(TokenType::Number, input_.substr(start, position_ - start), value);
    }

    if (std::isalpha(static_cast<unsigned char>(current))) {
        size_t start = position_;
        while (std::isalnum(static_cast<unsigned char>(peek()))) {
            consume();
        }
        return Token(TokenType::Variable, input_.substr(start, position_ - start), 0);
    }

    consume();
    switch (current) {
        case '+': return Token(TokenType::Plus, "+", 0);
        case '-': return Token(TokenType::Minus, "-", 0);
        case '=': return Token(TokenType::Equals, "=", 0);
        default:
            throw std::invalid_argument("Invalid character in expression: " + std::string(1, current));
    }
}

std::vector<Token> Lexer::tokenize() {
    std::vector<Token> tokens;
    while (true) {
        Token token = nextToken();
        if (token.type == TokenType::End) {
            break;
        }
        tokens.push_back(std::move(token));
    }
    return tokens;
}

} // namespace quant
