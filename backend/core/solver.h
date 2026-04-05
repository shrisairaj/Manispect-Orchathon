#ifndef QUANTSOLVE_SOLVER_H
#define QUANTSOLVE_SOLVER_H

#include <functional>
#include <map>
#include <string>
#include <unordered_map>
#include <vector>

namespace quant {

struct SolverResult {
    int totalSolutions = 0;
    std::vector<std::map<std::string, int>> solutions;
};

class Solver {
public:
    SolverResult solve(
        const std::unordered_map<std::string, int> &coefficients,
        int target,
        int displayLimit,
        const std::function<bool(const std::map<std::string, int> &)> &validator);

private:
    void backtrack(
        int index,
        int remainingTarget,
        const std::vector<std::pair<std::string, int>> &vars,
        std::vector<int> &assignment,
        const std::function<bool(const std::map<std::string, int> &)> &validator,
        SolverResult &result,
        int displayLimit);

    static int gcd(int a, int b);
    static int gcdOfRange(const std::vector<int> &values, int startIndex);
};

} // namespace quant

#endif // QUANTSOLVE_SOLVER_H
