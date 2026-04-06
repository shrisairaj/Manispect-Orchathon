# TODO: Fix Backend CORS for Production

## Plan Steps:
1. [ ] Create TODO-CORS.md (current)
2. [ ] Edit backend/server.cpp: Add full CORS headers to all responses, fix OPTIONS preflight, PORT env, request logging
3. [ ] Rebuild backend: cd backend && make clean && make
4. [ ] Test locally: curl -X OPTIONS http://localhost:8080/solve -v (check CORS headers)
5. [ ] Test POST API call from frontend localhost
6. [ ] Deploy to Render, test prod frontend->backend
7. [ ] Update TODO & complete
