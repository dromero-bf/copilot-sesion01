from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.users import router as users_router

app = FastAPI(
    title="JWT Authentication API",
    description="FastAPI application demonstrating JWT-based authentication.",
    version="0.1.0",
)

app.include_router(auth_router)
app.include_router(users_router)


@app.get("/", tags=["health"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
