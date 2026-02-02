"""
API router for cost code operations.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.models import CostCode, CostCategory
from app.data.cost_codes import cost_code_db

router = APIRouter(prefix="/cost-codes", tags=["Cost Codes"])


@router.get("/", response_model=List[CostCode])
async def list_cost_codes(
    category: Optional[CostCategory] = Query(None, description="Filter by category")
):
    """
    List all cost codes, optionally filtered by category.
    """
    if category:
        return cost_code_db.get_by_category(category)
    return cost_code_db.get_all()


@router.get("/categories", response_model=List[str])
async def list_categories():
    """
    List all available cost code categories.
    """
    return [cat.value for cat in CostCategory]


@router.get("/search", response_model=List[CostCode])
async def search_cost_codes(
    q: str = Query(..., description="Search query for code or description")
):
    """
    Search cost codes by code or description.
    """
    results = cost_code_db.search(q)
    if not results:
        raise HTTPException(status_code=404, detail="No cost codes found matching query")
    return results


@router.get("/{code}", response_model=CostCode)
async def get_cost_code(code: str):
    """
    Get a specific cost code by its code.
    """
    cost_code = cost_code_db.get_by_code(code)
    if not cost_code:
        raise HTTPException(status_code=404, detail=f"Cost code {code} not found")
    return cost_code
