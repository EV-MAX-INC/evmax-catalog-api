"""
API router for bid calculations.
"""
from fastapi import APIRouter
from app.models import ProjectSpecification, BidCalculation
from app.services import BidCalculationService

router = APIRouter(prefix="/bids", tags=["Bid Calculations"])
bid_service = BidCalculationService()


@router.post("/calculate", response_model=BidCalculation)
async def calculate_bid(project_spec: ProjectSpecification):
    """
    Calculate a complete bid for an EV charging station project.
    
    The bid includes:
    - Base material and labor costs
    - 10% material markup
    - 18% overhead
    - 15% GA excavation contingency
    - 27% target profit margin
    - Per-port and total project costs
    """
    return bid_service.calculate_bid(project_spec)
