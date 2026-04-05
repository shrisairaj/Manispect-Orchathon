# Quick Start Guide

## Build the C++ Backend

```bash
cd backend
make
```

OR manually:
```bash
cd backend
g++ -std=c++17 server.cpp core/lexer.cpp core/parser.cpp core/solver.cpp core/constraints.cpp core/engine.cpp -o server -lpthread
```

## Run Everything

### Terminal 1: Start C++ Backend
```bash
cd backend
./server 5000
```

Output:
```
QuantSolve C++ Backend Server
Listening on port 5000
```

### Terminal 2: Start React Frontend
```bash
cd frontend
npm run dev
```

Output:
```
  VITE v4.x.x  ready in 100 ms

  ➜  Local:   http://localhost:5173/
```

### Open in Browser
Go to `http://localhost:5173/`

## Test Backend Directly (Optional)

```bash
curl -X POST http://localhost:5000/solve \
  -H "Content-Type: application/json" \
  -d '{
    "expression": "10a + 5b = 50",
    "constraints": [],
    "displayLimit": 5
  }'
```

Expected response:
```json
{
  "totalSolutions": 6,
  "shownSolutions": 5,
  "solutions": [
    {"a": 0, "b": 10},
    {"a": 1, "b": 8},
    {"a": 2, "b": 6},
    {"a": 3, "b": 4},
    {"a": 4, "b": 2}
  ]
}
```

## Clean Build

```bash
cd backend
make clean
make
```

## All Python Files Have Been Removed ✓

- ✓ Deleted all `.py` files from `backend/`
- ✓ Deleted all `.py` files from `backend/core/`
- ✓ Deleted `requirements.txt`
- ✓ 100% C++ backend now
