#include "solver.h"
#include <algorithm>
#include <stdexcept>

namespace quant {

int Solver::gcd(int a, int b) {
    if (a < 0) a = -a;
    if (b < 0) b = -b;
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

int Solver::gcdOfRange(const std::vector<int> &values, int startIndex) {
    if (startIndex >= static_cast<int>(values.size())) {
        return 0;
    }
    int currentGcd = values[startIndex];
    for (size_t i = startIndex + 1; i < values.size(); ++i) {
        currentGcd = gcd(currentGcd, values[i]);
        if (currentGcd == 1) {
            break;
        }
    }
    return currentGcd;
}

SolverResult Solver::solve(
    const std::unordered_map<std::string, int> &coefficients,
    int target,
    int displayLimit,
    const std::function<bool(const std::map<std::string, int> &)> &validator) {
    if (target < 0) {
        return {};
    }

    std::vector<std::pair<std::string, int>> vars;
    vars.reserve(coefficients.size());
    for (const auto &entry : coefficients) {
        if (entry.second == 0) {
            continue;
        }
        if (entry.second < 0) {
            throw std::invalid_argument("Negative coefficients are not supported in the solver.");
        }
        vars.emplace_back(entry.first, entry.second);
    }

    std::sort(vars.begin(), vars.end(), [](const auto &a, const auto &b) {
        return a.second > b.second;
    });

    SolverResult result;
    std::vector<int> assignment(vars.size(), 0);
    backtrack(0, target, vars, assignment, validator, result, displayLimit);
    return result;
}

void Solver::backtrack(
    int index,
    int remainingTarget,
    const std::vector<std::pair<std::string, int>> &vars,
    std::vector<int> &assignment,
    const std::function<bool(const std::map<std::string, int> &)> &validator,
    SolverResult &result,
    int displayLimit) {
    if (remainingTarget < 0) {
        return;
    }

    int varCount = static_cast<int>(vars.size());
    if (index == varCount) {
        if (remainingTarget != 0) {
            return;
        }
        std::map<std::string, int> solution;
        for (int i = 0; i < varCount; ++i) {
            solution[vars[i].first] = assignment[i];
        }
        if (validator(solution)) {
            ++result.totalSolutions;
            if (static_cast<int>(result.solutions.size()) < displayLimit) {
                result.solutions.push_back(solution);
            }
        }
        return;
    }

    int coefficient = vars[index].second;
    int maxValue = remainingTarget / coefficient;

    std::vector<int> tailCoefficients;
    tailCoefficients.reserve(varCount - index - 1);
    for (int i = index + 1; i < varCount; ++i) {
        tailCoefficients.push_back(vars[i].second);
    }
    int tailGcd = gcdOfRange(tailCoefficients, 0);

    for (int value = 0; value <= maxValue; ++value) {
        int nextTarget = remainingTarget - value * coefficient;
        if (!tailCoefficients.empty() && tailGcd > 1 && nextTarget % tailGcd != 0) {
            continue;
        }
        assignment[index] = value;
        backtrack(index + 1, nextTarget, vars, assignment, validator, result, displayLimit);
    }
}

} // namespace quant
