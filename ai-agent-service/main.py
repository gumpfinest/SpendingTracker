"""
SmartSpend AI Agent Service
---------------------------
FastAPI microservice for AI-powered financial advice and chat functionality.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api import advice, chat, patterns
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    print("AI Agent Service starting up...")
    yield
    print("AI Agent Service shutting down...")


app = FastAPI(
    title="SmartSpend AI Agent Service",
    description="AI-powered financial assistant microservice for SmartSpend",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(advice.router, prefix="/api", tags=["Financial Advice"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(patterns.router, prefix="/api", tags=["Pattern Analysis"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "SmartSpend AI Agent Service",
        "version": "1.0.0",
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
