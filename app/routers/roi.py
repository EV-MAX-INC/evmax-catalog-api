"""
API router for ROI analysis and financial projections.
"""
from typing import Optional
from fastapi import APIRouter, Query
from app.models import ProjectSpecification, ROIAnalysis
from app.services import BidCalculationService, ROIAnalysisService

router = APIRouter(prefix="/roi", tags=["ROI Analysis"])
bid_service = BidCalculationService()
roi_service = ROIAnalysisService()


@router.post("/analyze", response_model=ROIAnalysis)
async def analyze_roi(
    project_spec: ProjectSpecification,
    annual_revenue_per_port: float = Query(5000.0, description="Expected annual revenue per port", gt=0),
    annual_operating_cost_per_port: float = Query(800.0, description="Annual operating cost per port", ge=0)
):
    """
    Calculate ROI and financial projections for an EV charging station project.
    
    Provides:
    - Payback period
    - Annual ROI percentage
    - 10-year net profit projections
    - 10-year ROI percentage
    
    Default assumptions:
    - $5,000 annual revenue per port
    - $800 annual operating cost per port
    """
    # First calculate the bid
    bid = bid_service.calculate_bid(project_spec)
    
    # Then calculate ROI
    return roi_service.calculate_roi(
        bid=bid,
        annual_revenue_per_port=annual_revenue_per_port,
        annual_operating_cost_per_port=annual_operating_cost_per_port
    )
