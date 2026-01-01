"""
SmartSpend Data Service
----------------------
FastAPI microservice for transaction categorization, spending analysis, and forecasting.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api import categorize, forecast, analyze
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    print("Data Service starting up...")
    yield
    # Shutdown
    print("Data Service shutting down...")


app = FastAPI(
    title="SmartSpend Data Service",
    description="Data processing and analytics microservice for SmartSpend",
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
app.include_router(categorize.router, prefix="/api", tags=["Categorization"])
app.include_router(forecast.router, prefix="/api", tags=["Forecasting"])
app.include_router(analyze.router, prefix="/api", tags=["Analysis"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "SmartSpend Data Service",
        "version": "1.0.0",
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
