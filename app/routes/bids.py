"""Bid API routes."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.bid import (
    BidCreate,
    BidUpdate,
    BidResponse,
    BidList,
    BidCalculateRequest,
    BidCalculateResponse,
    ROIAnalysisRequest,
    ROIAnalysisResponse,
)
from app.services.bid_service import BidService
from app.config import settings

router = APIRouter(prefix="/bids", tags=["Bids"])


@router.get("", response_model=BidList)
def list_bids(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(
        settings.DEFAULT_PAGE_SIZE,
        ge=1,
        le=settings.MAX_PAGE_SIZE,
        description="Items per page",
    ),
    status: Optional[str] = Query(None, description="Filter by status"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db),
):
    """
    Get a list of bids with optional filtering and pagination.
    
    - **page**: Page number (starts at 1)
    - **page_size**: Number of items per page
    - **status**: Filter by status (draft, submitted, accepted, rejected)
    - **is_active**: Filter by active status
    """
    skip = (page - 1) * page_size
    bids, total = BidService.get_bids(
        db=db,
        skip=skip,
        limit=page_size,
        status=status,
        is_active=is_active,
    )

    pages = (total + page_size - 1) // page_size

    return BidList(
        items=bids,
        total=total,
        page=page,
        page_size=page_size,
        pages=pages,
    )


@router.get("/{bid_id}", response_model=BidResponse)
def get_bid(
    bid_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a specific bid by ID.
    
    - **bid_id**: Bid ID
    """
    bid = BidService.get_bid(db, bid_id)
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    return bid


@router.post("", response_model=BidResponse, status_code=201)
def create_bid(
    bid_data: BidCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new bid.
    
    - **project_name**: Project name
    - **client_name**: Client name (optional)
    - **line_items**: List of bid line items
    - **tax_rate**: Tax rate percentage
    """
    if not settings.ENABLE_BID_CALCULATION:
        raise HTTPException(
            status_code=403,
            detail="Bid calculation is currently disabled",
        )

    bid = BidService.create_bid(db, bid_data)
    return bid


@router.put("/{bid_id}", response_model=BidResponse)
def update_bid(
    bid_id: int,
    bid_data: BidUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing bid.
    
    - **bid_id**: Bid ID
    """
    bid = BidService.update_bid(db, bid_id, bid_data)
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found")
    return bid


@router.delete("/{bid_id}", status_code=204)
def delete_bid(
    bid_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a bid (soft delete).
    
    - **bid_id**: Bid ID
    """
    success = BidService.delete_bid(db, bid_id)
    if not success:
        raise HTTPException(status_code=404, detail="Bid not found")


@router.post("/calculate", response_model=BidCalculateResponse)
def calculate_bid(
    request: BidCalculateRequest,
    db: Session = Depends(get_db),
):
    """
    Calculate bid totals from cost codes without creating a bid.
    
    - **line_items**: List of items with cost_code_id and quantity
    - **tax_rate**: Tax rate percentage
    """
    if not settings.ENABLE_BID_CALCULATION:
        raise HTTPException(
            status_code=403,
            detail="Bid calculation is currently disabled",
        )

    result = BidService.calculate_bid_from_cost_codes(
        db=db,
        line_items=request.line_items,
        tax_rate=request.tax_rate,
    )

    return BidCalculateResponse(**result)


# ROI Analysis Router
analysis_router = APIRouter(prefix="/analysis", tags=["ROI Analysis"])


@analysis_router.post("/roi", response_model=ROIAnalysisResponse)
def calculate_roi(
    request: ROIAnalysisRequest,
):
    """
    Calculate ROI analysis for a project.
    
    - **estimated_revenue**: Estimated project revenue
    - **estimated_cost**: Estimated project cost
    - **project_duration_months**: Project duration in months
    """
    if not settings.ENABLE_ROI_ANALYSIS:
        raise HTTPException(
            status_code=403,
            detail="ROI analysis is currently disabled",
        )

    result = BidService.calculate_roi_analysis(
        estimated_revenue=request.estimated_revenue,
        estimated_cost=request.estimated_cost,
        project_duration_months=request.project_duration_months,
    )

    return ROIAnalysisResponse(**result)
