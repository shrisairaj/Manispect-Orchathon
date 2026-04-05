#include "constraints.h"
#include <algorithm>
#include <cctype>
#include <stdexcept>

namespace quant {

static std::string trim(const std::string &value) {
    size_t start = 0;
    while (start < value.size() && std::isspace(static_cast<unsigned char>(value[start]))) {
        ++start;
    }
    size_t end = value.size();
    while (end > start && std::isspace(static_cast<unsigned char>(value[end - 1]))) {
        --end;
    }
    return value.substr(start, end - start);
}

static Comparator parseComparator(const std::string &text) {
    if (text == ">=") return Comparator::GreaterEqual;
    if (text == "<=") return Comparator::LessEqual;
    if (text == ">") return Comparator::Greater;
    if (text == "<") return Comparator::Less;
    if (text == "=" || text == "==") return Comparator::Equal;
    throw std::invalid_argument("Unsupported comparator: " + text);
}

bool Constraint::evaluate(const std::map<std::string, int> &solution) const {
    int value = 0;
    auto it = solution.find(variable);
    if (it != solution.end()) {
        value = it->second;
    }

    switch (comparator) {
        case Comparator::GreaterEqual: return value >= bound;
        case Comparator::LessEqual: return value <= bound;
        case Comparator::Greater: return value > bound;
        case Comparator::Less: return value < bound;
        case Comparator::Equal: return value == bound;
    }
    return false;
}

std::vector<Constraint> parseConstraints(const std::vector<std::string> &constraintStrings) {
    std::vector<Constraint> constraints;
    for (const auto &raw : constraintStrings) {
        std::string input = trim(raw);
        std::string comparatorText;
        size_t pos = std::string::npos;

        for (const auto &candidate : {std::string(">="), std::string("<="), std::string("=="), std::string("="), std::string(">"), std::string("<")}) {
            pos = input.find(candidate);
            if (pos != std::string::npos) {
                comparatorText = candidate;
                break;
            }
        }

        if (pos == std::string::npos) {
            throw std::invalid_argument("Constraint missing comparator: " + raw);
        }

        std::string left = trim(input.substr(0, pos));
        std::string right = trim(input.substr(pos + comparatorText.size()));
        if (left.empty() || right.empty()) {
            throw std::invalid_argument("Malformed constraint: " + raw);
        }

        int bound = std::stoi(right);
        constraints.push_back(Constraint{left, parseComparator(comparatorText), bound});
    }
    return constraints;
}

bool isValid(const std::map<std::string, int> &solution, const std::vector<Constraint> &constraints) {
    for (const auto &constraint : constraints) {
        if (!constraint.evaluate(solution)) {
            return false;
        }
    }
    return true;
}

} // namespace quant
