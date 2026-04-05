#include "parser.h"
#include <stdexcept>

namespace quant {

static Expression makeConstant(int value) {
    Expression expr;
    expr.constant = value;
    return expr;
}

static Expression makeVariable(const std::string &name, int coefficient = 1) {
    Expression expr;
    expr.coefficients[name] = coefficient;
    return expr;
}

Expression Parser::add(const Expression &lhs, const Expression &rhs) {
    Expression result = lhs;
    result.constant += rhs.constant;
    for (const auto &entry : rhs.coefficients) {
        result.coefficients[entry.first] += entry.second;
        if (result.coefficients[entry.first] == 0) {
            result.coefficients.erase(entry.first);
        }
    }
    return result;
}

Expression Parser::subtract(const Expression &lhs, const Expression &rhs) {
    Expression result = lhs;
    result.constant -= rhs.constant;
    for (const auto &entry : rhs.coefficients) {
        result.coefficients[entry.first] -= entry.second;
        if (result.coefficients[entry.first] == 0) {
            result.coefficients.erase(entry.first);
        }
    }
    return result;
}

Expression Parser::multiply(const Expression &lhs, const Expression &rhs) {
    bool lhsHasVars = !lhs.coefficients.empty();
    bool rhsHasVars = !rhs.coefficients.empty();
    if (lhsHasVars && rhsHasVars) {
        throw std::invalid_argument("Multiplication of two variables is not supported.");
    }

    if (lhsHasVars) {
        int scalar = rhs.constant;
        if (scalar == 0) {
            return makeConstant(0);
        }
        Expression result;
        result.constant = lhs.constant * scalar;
        for (const auto &entry : lhs.coefficients) {
            result.coefficients[entry.first] = entry.second * scalar;
        }
        return result;
    }

    if (rhsHasVars) {
        int scalar = lhs.constant;
        if (scalar == 0) {
            return makeConstant(0);
        }
        Expression result;
        result.constant = rhs.constant * scalar;
        for (const auto &entry : rhs.coefficients) {
            result.coefficients[entry.first] = entry.second * scalar;
        }
        return result;
    }

    return makeConstant(lhs.constant * rhs.constant);
}

Expression Parser::divide(const Expression &lhs, const Expression &rhs) {
    if (!rhs.coefficients.empty()) {
        throw std::invalid_argument("Division by a variable expression is not supported.");
    }
    if (rhs.constant == 0) {
        throw std::invalid_argument("Division by zero is not allowed.");
    }
    if (lhs.constant % rhs.constant != 0) {
        throw std::invalid_argument("Expression must evaluate to whole numbers only.");
    }
    Expression result;
    result.constant = lhs.constant / rhs.constant;
    for (const auto &entry : lhs.coefficients) {
        if (entry.second % rhs.constant != 0) {
            throw std::invalid_argument("Expression must evaluate to whole numbers only.");
        }
        result.coefficients[entry.first] = entry.second / rhs.constant;
    }
    return result;
}

ParseResult Parser::parseEquation(const std::string &expression) {
    Lexer lexer(expression);
    auto tokens = lexer.tokenize();

    size_t equalsIndex = tokens.size();
    for (size_t i = 0; i < tokens.size(); ++i) {
        if (tokens[i].type == TokenType::Equals) {
            equalsIndex = i;
            break;
        }
    }

    if (equalsIndex == tokens.size()) {
        throw std::invalid_argument("Expression must contain '=' to separate sides.");
    }

    size_t leftIndex = 0;
    Expression leftExpr = parseExpression(tokens, leftIndex, equalsIndex);
    if (leftIndex != equalsIndex) {
        throw std::invalid_argument("Invalid expression on left side of '='.");
    }

    size_t rightIndex = equalsIndex + 1;
    Expression rightExpr = parseExpression(tokens, rightIndex, tokens.size());
    if (rightIndex != tokens.size()) {
        throw std::invalid_argument("Invalid expression on right side of '='.");
    }

    ParseResult result;
    result.coefficients = leftExpr.coefficients;
    for (const auto &entry : rightExpr.coefficients) {
        result.coefficients[entry.first] -= entry.second;
    }
    result.target = rightExpr.constant - leftExpr.constant;

    for (auto it = result.coefficients.begin(); it != result.coefficients.end();) {
        if (it->second == 0) {
            it = result.coefficients.erase(it);
        } else {
            ++it;
        }
    }

    return result;
}

Expression Parser::parseExpression(const std::vector<Token> &tokens, size_t &index, size_t end) {
    Expression result = parseTerm(tokens, index, end);
    while (index < end && (tokens[index].type == TokenType::Plus || tokens[index].type == TokenType::Minus)) {
        TokenType op = tokens[index].type;
        ++index;
        Expression rhs = parseTerm(tokens, index, end);
        result = (op == TokenType::Plus) ? add(result, rhs) : subtract(result, rhs);
    }
    return result;
}

Expression Parser::parseTerm(const std::vector<Token> &tokens, size_t &index, size_t end) {
    Expression result = parseFactor(tokens, index, end);
    while (index < end && (tokens[index].type == TokenType::Multiply || tokens[index].type == TokenType::Divide)) {
        TokenType op = tokens[index].type;
        ++index;
        Expression rhs = parseFactor(tokens, index, end);
        result = (op == TokenType::Multiply) ? multiply(result, rhs) : divide(result, rhs);
    }
    return result;
}

Expression Parser::parseFactor(const std::vector<Token> &tokens, size_t &index, size_t end) {
    if (index >= end) {
        throw std::invalid_argument("Unexpected end of expression.");
    }

    if (tokens[index].type == TokenType::Plus || tokens[index].type == TokenType::Minus) {
        TokenType sign = tokens[index].type;
        ++index;
        Expression factor = parseFactor(tokens, index, end);
        if (sign == TokenType::Minus) {
            for (auto &entry : factor.coefficients) {
                entry.second = -entry.second;
            }
            factor.constant = -factor.constant;
        }
        return factor;
    }

    if (tokens[index].type == TokenType::Number) {
        int value = static_cast<int>(tokens[index].value);
        ++index;
        if (index < end && tokens[index].type == TokenType::Variable) {
            std::string variable = tokens[index].text;
            ++index;
            return makeVariable(variable, value);
        }
        return makeConstant(value);
    }

    if (tokens[index].type == TokenType::Variable) {
        std::string variable = tokens[index].text;
        ++index;
        return makeVariable(variable, 1);
    }

    if (tokens[index].type == TokenType::LeftParen) {
        ++index;
        Expression inner = parseExpression(tokens, index, end);
        if (index >= end || tokens[index].type != TokenType::RightParen) {
            throw std::invalid_argument("Mismatched parentheses in expression.");
        }
        ++index;
        return inner;
    }

    throw std::invalid_argument("Unexpected token in expression.");
}

} // namespace quant
