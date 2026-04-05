#ifndef QUANTSOLVE_PARSER_H
#define QUANTSOLVE_PARSER_H

#include "lexer.h"
#include <string>
#include <unordered_map>

namespace quant {

struct ParseResult {
    std::unordered_map<std::string, int> coefficients;
    int target = 0;
};

class Parser {
public:
    ParseResult parseEquation(const std::string &expression);

private:
    struct Side {
        std::unordered_map<std::string, int> coefficients;
        int constant = 0;
    };

    Side parseSide(const std::vector<Token> &tokens, size_t start, size_t end);
    void accumulateTerm(Side &side, const std::string &variable, int coefficient, int sign);
};

} // namespace quant

#endif // QUANTSOLVE_PARSER_H
