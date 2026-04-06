# TODO: Fix CORS & Production API for Backend/Frontend

## Information Gathered:
- server.cpp: Partial CORS (missing full headers on 404, incomplete OPTIONS), no PORT env, no logging.
- App.jsx: Placeholder URL causing fetch fail.

## Plan:
- Add PORT=getenv("PORT") || 8080 in main()
- Add CORS to all responses (*, GET POST OPTIONS, Content-Type)
- Handle OPTIONS preflight 200
- Log requests
- Frontend: Use import.meta.env.VITE_API_URL + '/solve'
- Create .env: VITE_API_URL=https://your-app.onrender.com
- Bind 0.0.0.0 confirmed.

## Dependent Files:
- backend/server.cpp (main)
- frontend/src/App.jsx (API URL)
- frontend/.env (new)

## Followup:
- make clean && make && ./backend/server
- Deploy Render/Vercel
- Test prod fetch

Confirm plan?
