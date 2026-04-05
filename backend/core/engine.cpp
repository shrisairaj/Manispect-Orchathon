#include "engine.h"
#include "constraints.h"
#include "parser.h"
#include "solver.h"

#include <iostream>

namespace quant {

EngineResult solve_equation(
    const std::string &expression,
    const std::vector<std::string> &constraints,
    int displayLimit) {
    Parser parser;
    ParseResult parseResult = parser.parseEquation(expression);

    std::vector<Constraint> parsedConstraints = parseConstraints(constraints);
    auto validator = [&parsedConstraints](const std::map<std::string, int> &solution) {
        return isValid(solution, parsedConstraints);
    };

    Solver solver;
    SolverResult solverResult = solver.solve(parseResult.coefficients, parseResult.target, displayLimit, validator);

    EngineResult output;
    output.totalSolutions = solverResult.totalSolutions;
    output.shownSolutions = static_cast<int>(solverResult.solutions.size());
    output.solutions = std::move(solverResult.solutions);
    return output;
}

} // namespace quant
