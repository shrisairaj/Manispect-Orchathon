#ifndef QUANTSOLVE_CONSTRAINTS_H
#define QUANTSOLVE_CONSTRAINTS_H

#include <map>
#include <string>
#include <vector>

namespace quant {

enum class Comparator {
    GreaterEqual,
    LessEqual,
    Greater,
    Less,
    Equal
};

struct Constraint {
    std::string variable;
    Comparator comparator;
    int bound;

    bool evaluate(const std::map<std::string, int> &solution) const;
};

std::vector<Constraint> parseConstraints(const std::vector<std::string> &constraintStrings);
bool isValid(const std::map<std::string, int> &solution, const std::vector<Constraint> &constraints);

} // namespace quant

#endif // QUANTSOLVE_CONSTRAINTS_H
