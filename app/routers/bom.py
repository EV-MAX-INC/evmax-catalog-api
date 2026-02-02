"""
API router for BOM generation.
"""
from typing import List
from fastapi import APIRouter
from app.models import BOMLineItem, ProjectSpecification
from app.services import BOMService

router = APIRouter(prefix="/bom", tags=["Bill of Materials"])
bom_service = BOMService()


@router.post("/generate", response_model=List[BOMLineItem])
async def generate_bom(project_spec: ProjectSpecification):
    """
    Generate a Bill of Materials (BOM) based on project specifications.
    
    The BOM includes all necessary materials, labor, and equipment needed
    for the EV charging station installation.
    """
    return bom_service.generate_bom(project_spec)
