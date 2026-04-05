#ifndef QUANTSOLVE_LEXER_H
#define QUANTSOLVE_LEXER_H

#include <string>
#include <vector>

namespace quant {

enum class TokenType {
    Number,
    Variable,
    Plus,
    Minus,
    Equals,
    End,
    Invalid
};

struct Token {
    TokenType type;
    std::string text;
    long long value;

    Token(TokenType type = TokenType::Invalid, std::string text = "", long long value = 0)
        : type(type), text(std::move(text)), value(value) {}
};

class Lexer {
public:
    explicit Lexer(std::string input);
    std::vector<Token> tokenize();

private:
    const std::string input_;
    size_t position_ = 0;

    char peek() const;
    char consume();
    void skipWhitespace();
    Token nextToken();
};

} // namespace quant

#endif // QUANTSOLVE_LEXER_H
