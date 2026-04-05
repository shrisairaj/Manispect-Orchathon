from fastapi import FastAPI
from backend.api.routes import router as api_router

app = FastAPI(
    title="QuantSolve API",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Backend is running"}