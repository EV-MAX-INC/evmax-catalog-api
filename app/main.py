from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from contextlib import asynccontextmanager
from app.config import settings
from app.database import get_db, init_db
from app.routers import products
from app import schemas


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager"""
    # Startup: Initialize database
    init_db()
    yield
    # Shutdown: cleanup if needed
    pass


# Initialize FastAPI app
app = FastAPI(
    title="EV MAX Catalog API",
    description="Product catalog and quote generation API for precast concrete products",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(products.router)


@app.get("/", tags=["root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to EV MAX Catalog API",
        "version": "2.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=schemas.HealthCheck, tags=["health"])
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return schemas.HealthCheck(
        status="healthy" if db_status == "healthy" else "unhealthy",
        database=db_status,
        timestamp=datetime.now()
    )
