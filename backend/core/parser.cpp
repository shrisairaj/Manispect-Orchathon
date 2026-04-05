#include "parser.h"
#include <stdexcept>

namespace quant {

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

    Side left = parseSide(tokens, 0, equalsIndex);
    Side right = parseSide(tokens, equalsIndex + 1, tokens.size());

    ParseResult result;
    for (const auto &pair : left.coefficients) {
        result.coefficients[pair.first] += pair.second;
    }
    for (const auto &pair : right.coefficients) {
        result.coefficients[pair.first] -= pair.second;
    }
    result.target = right.constant - left.constant;

    for (auto it = result.coefficients.begin(); it != result.coefficients.end();) {
        if (it->second == 0) {
            it = result.coefficients.erase(it);
        } else {
            ++it;
        }
    }

    return result;
}

Parser::Side Parser::parseSide(const std::vector<Token> &tokens, size_t start, size_t end) {
    Side side;
    int sign = 1;
    size_t index = start;

    while (index < end) {
        if (tokens[index].type == TokenType::Plus) {
            sign = 1;
            ++index;
            continue;
        }
        if (tokens[index].type == TokenType::Minus) {
            sign = -1;
            ++index;
            continue;
        }

        int coefficient = 0;
        bool hasNumber = false;
        std::string variable;

        if (index < end && tokens[index].type == TokenType::Number) {
            coefficient = static_cast<int>(tokens[index].value);
            hasNumber = true;
            ++index;
        }

        if (index < end && tokens[index].type == TokenType::Variable) {
            variable = tokens[index].text;
            ++index;
        }

        if (!hasNumber) {
            coefficient = variable.empty() ? 0 : 1;
        }

        accumulateTerm(side, variable, coefficient, sign);
        sign = 1;
    }

    return side;
}

void Parser::accumulateTerm(Side &side, const std::string &variable, int coefficient, int sign) {
    if (variable.empty()) {
        side.constant += sign * coefficient;
    } else {
        side.coefficients[variable] += sign * coefficient;
    }
}

} // namespace quant
