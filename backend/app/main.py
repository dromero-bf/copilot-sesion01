from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.users import router as users_router

app = FastAPI(
    title="JWT Authentication API",
    description="FastAPI application demonstrating JWT-based authentication.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)


@app.get("/", tags=["health"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
