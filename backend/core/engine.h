#ifndef QUANTSOLVE_ENGINE_H
#define QUANTSOLVE_ENGINE_H

#include "constraints.h"
#include "parser.h"
#include "solver.h"
#include <string>
#include <vector>

namespace quant {

struct EngineResult {
    int totalSolutions = 0;
    int shownSolutions = 0;
    std::vector<std::map<std::string, int>> solutions;
};

EngineResult solve_equation(
    const std::string &expression,
    const std::vector<std::string> &constraints,
    int displayLimit = 10);

} // namespace quant

#endif // QUANTSOLVE_ENGINE_H
