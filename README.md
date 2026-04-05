# QuantSolve

A high-performance linear equation solver with integer solutions and constraints.

## Features

- Parse linear equations with variables
- Find all non-negative integer solutions
- Apply constraints (≥, ≤, >, <, =)
- Optimized backtracking with GCD pruning
- Web interface with React frontend
- REST API with C++ backend (High performance)

## Architecture

- **Frontend**: React + Vite (JavaScript)
- **Backend**: C++ with HTTP server
- **Core**: Lexer → Parser → Solver → Constraint Engine

## Project Structure

```
QuantSolve/
├── backend/
│   ├── core/              # C++ core implementation
│   │   ├── lexer.h/cpp
│   │   ├── parser.h/cpp
│   │   ├── solver.h/cpp
│   │   ├── constraints.h/cpp
│   │   └── engine.h/cpp
│   ├── server.cpp         # C++ HTTP server
│   ├── Makefile
│   └── server             # Compiled binary
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Setup & Running

### Build C++ Backend

```bash
cd backend
make clean && make
```

Or with explicit compilation:
```bash
g++ -std=c++17 server.cpp core/lexer.cpp core/parser.cpp core/solver.cpp core/constraints.cpp core/engine.cpp -o server -lpthread
```

### Run Backend Server

```bash
cd backend
./server 5000
```

Server will listen on `http://localhost:5000`

### Setup Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend will run on `http://localhost:5173` (or next available port)

## API Endpoints

### POST `/solve`

**Request:**
```json
{
  "expression": "10a + 15b + 20c + 50d + 5e = 1000",
  "constraints": ["a >= 2", "b <= 10"],
  "displayLimit": 10
}
```

**Response:**
```json
{
  "totalSolutions": 157102,
  "shownSolutions": 10,
  "solutions": [
    {"a": 2, "b": 0, "c": 0, "d": 0, "e": 196},
    {"a": 3, "b": 0, "c": 0, "d": 0, "e": 194},
    ...
  ]
}
```

## CLI Usage

Test equation directly without frontend:

```bash
cd backend
./server 5000 &
sleep 1

curl -X POST http://localhost:5000/solve \
  -H "Content-Type: application/json" \
  -d '{
    "expression": "10a + 5b = 100",
    "constraints": ["a >= 2"],
    "displayLimit": 5
  }'
```

## Performance

- **Lexer**: O(n) tokenization
- **Parser**: O(n) parsing to coefficients
- **Solver**: O(n!) worst case with GCD pruning optimization
- **Constraints**: O(k) validation per solution

## Example

Equation: `10a + 15b + 20c = 100`
Constraints: `a >= 1`, `b <= 5`

Will find all non-negative integer solutions where:
- `10*a + 15*b + 20*c = 100`
- `a >= 1` and `b <= 5`
- Display first 10 solutions

---

**Built with C++17 for performance and React for modern UI.**
