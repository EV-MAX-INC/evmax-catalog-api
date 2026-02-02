"""
EV MAX Catalog API - Main application entry point.

A SaaS-ready catalog API for managing and serving EV charging station 
installation cost data with automated bid calculations and ROI analysis.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import cost_codes, bom, bids, roi, benchmarks

# Create FastAPI application
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="""
    ## EV MAX Catalog API
    
    A comprehensive catalog API for EV charging station installation cost management.
    
    ### Features
    
    * **Cost Code Management**: 83+ cost codes across 9 categories
    * **BOM Generation**: Automated bill of materials creation
    * **Bid Calculations**: Complete bid calculations with industry-standard markups
    * **ROI Analysis**: Financial projections and payback period calculations
    * **Benchmark Comparisons**: Compare pricing against industry competitors
    
    ### Cost Categories
    
    1. **Concrete** (CONC-001 to CONC-010)
    2. **Conduit** (COND-001 to COND-015)
    3. **Wire** (WIRE-001 to WIRE-012)
    4. **Labor** (LABOR-001 to LABOR-010)
    5. **Equipment** (EQUIP-001 to EQUIP-015)
    6. **Safety** (SAFE-001 to SAFE-008)
    7. **Site** (SITE-001 to SITE-010)
    8. **Restoration** (REST-001 to REST-008)
    9. **Grounding** (GRND-001 to GRND-007)
    
    ### Pricing Methodology
    
    * 10% material markup
    * 18% overhead calculation
    * 15% GA excavation contingency
    * 27% target profit margin
    
    ### Supported Infrastructure
    
    * **L2 Charging**: 7.2 kW and 19.2 kW chargers
    * **DC Fast Charging**: 50 kW, 150 kW, and 350 kW chargers
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(cost_codes.router)
app.include_router(bom.router)
app.include_router(bids.router)
app.include_router(roi.router)
app.include_router(benchmarks.router)


@app.get("/", tags=["Health"])
async def root():
    """
    API health check endpoint.
    """
    return {
        "status": "healthy",
        "api": settings.api_title,
        "version": settings.api_version,
        "endpoints": {
            "cost_codes": "/cost-codes",
            "bom": "/bom",
            "bids": "/bids",
            "roi": "/roi",
            "benchmarks": "/benchmarks",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Detailed health check endpoint.
    """
    from app.data.cost_codes import cost_code_db
    
    return {
        "status": "healthy",
        "api_version": settings.api_version,
        "cost_codes_loaded": len(cost_code_db.get_all()),
        "categories": len(list(settings.CostCategory)) if hasattr(settings, 'CostCategory') else 9,
        "configuration": {
            "material_markup": f"{settings.material_markup * 100}%",
            "overhead_rate": f"{settings.overhead_rate * 100}%",
            "ga_excavation_contingency": f"{settings.ga_excavation_contingency * 100}%",
            "target_profit_margin": f"{settings.target_profit_margin * 100}%",
            "roi_analysis_years": settings.roi_analysis_years
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
