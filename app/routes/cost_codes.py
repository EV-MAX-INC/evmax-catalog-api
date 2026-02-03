"""Cost code API routes."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.cost_code import (
    CostCodeCreate,
    CostCodeUpdate,
    CostCodeResponse,
    CostCodeList,
)
from app.services.cost_code_service import CostCodeService
from app.config import settings

router = APIRouter(prefix="/cost-codes", tags=["Cost Codes"])


@router.get("", response_model=CostCodeList)
def list_cost_codes(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(
        settings.DEFAULT_PAGE_SIZE,
        ge=1,
        le=settings.MAX_PAGE_SIZE,
        description="Items per page",
    ),
    category: Optional[str] = Query(None, description="Filter by category"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    search: Optional[str] = Query(None, description="Search in code, name, or description"),
    db: Session = Depends(get_db),
):
    """
    Get a list of cost codes with optional filtering and pagination.
    
    - **page**: Page number (starts at 1)
    - **page_size**: Number of items per page
    - **category**: Filter by category
    - **is_active**: Filter by active status
    - **search**: Search term
    """
    skip = (page - 1) * page_size
    cost_codes, total = CostCodeService.get_cost_codes(
        db=db,
        skip=skip,
        limit=page_size,
        category=category,
        is_active=is_active,
        search=search,
    )

    pages = (total + page_size - 1) // page_size

    return CostCodeList(
        items=cost_codes,
        total=total,
        page=page,
        page_size=page_size,
        pages=pages,
    )


@router.get("/{cost_code_id}", response_model=CostCodeResponse)
def get_cost_code(
    cost_code_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a specific cost code by ID.
    
    - **cost_code_id**: Cost code ID
    """
    cost_code = CostCodeService.get_cost_code(db, cost_code_id)
    if not cost_code:
        raise HTTPException(status_code=404, detail="Cost code not found")
    return cost_code


@router.post("", response_model=CostCodeResponse, status_code=201)
def create_cost_code(
    cost_code_data: CostCodeCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new cost code.
    
    - **code**: Unique cost code identifier
    - **name**: Cost code name
    - **category**: Cost code category
    - **unit**: Unit of measurement
    - **unit_price**: Price per unit
    """
    # Check if code already exists
    existing = CostCodeService.get_cost_code_by_code(db, cost_code_data.code)
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Cost code '{cost_code_data.code}' already exists",
        )

    cost_code = CostCodeService.create_cost_code(db, cost_code_data)
    return cost_code


@router.put("/{cost_code_id}", response_model=CostCodeResponse)
def update_cost_code(
    cost_code_id: int,
    cost_code_data: CostCodeUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing cost code.
    
    - **cost_code_id**: Cost code ID
    """
    cost_code = CostCodeService.update_cost_code(db, cost_code_id, cost_code_data)
    if not cost_code:
        raise HTTPException(status_code=404, detail="Cost code not found")
    return cost_code


@router.delete("/{cost_code_id}", status_code=204)
def delete_cost_code(
    cost_code_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a cost code (soft delete).
    
    - **cost_code_id**: Cost code ID
    """
    success = CostCodeService.delete_cost_code(db, cost_code_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cost code not found")
