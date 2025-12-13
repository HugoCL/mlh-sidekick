from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="MLH Sidekick API",
    description="Backend API for MLH Sidekick",
    version="0.1.0",
)


class HealthResponse(BaseModel):
    status: str
    message: str


@app.get("/")
def read_root():
    return {"message": "Welcome to MLH Sidekick API"}


@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="healthy",
        message="API is running"
    )
