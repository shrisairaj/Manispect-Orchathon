#ifndef QUANTSOLVE_PARSER_H
#define QUANTSOLVE_PARSER_H

#include "lexer.h"
#include <string>
#include <unordered_map>
#include <vector>

namespace quant {

struct ParseResult {
    std::unordered_map<std::string, int> coefficients;
    int target = 0;
};

struct Expression {
    std::unordered_map<std::string, int> coefficients;
    int constant = 0;
};

class Parser {
public:
    ParseResult parseEquation(const std::string &expression);

private:
    Expression parseExpression(const std::vector<Token> &tokens, size_t &index, size_t end);
    Expression parseTerm(const std::vector<Token> &tokens, size_t &index, size_t end);
    Expression parseFactor(const std::vector<Token> &tokens, size_t &index, size_t end);

    static Expression add(const Expression &lhs, const Expression &rhs);
    static Expression subtract(const Expression &lhs, const Expression &rhs);
    static Expression multiply(const Expression &lhs, const Expression &rhs);
    static Expression divide(const Expression &lhs, const Expression &rhs);
};

} // namespace quant

#endif // QUANTSOLVE_PARSER_H
