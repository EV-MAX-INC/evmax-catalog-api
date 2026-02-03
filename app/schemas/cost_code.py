"""Cost code Pydantic schemas for API validation."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class CostCodeBase(BaseModel):
    """Base cost code schema with common fields."""

    code: str = Field(..., min_length=1, max_length=50, description="Unique cost code identifier")
    name: str = Field(..., min_length=1, max_length=255, description="Cost code name")
    description: Optional[str] = Field(None, description="Detailed description")
    category: str = Field(..., min_length=1, max_length=100, description="Cost code category")
    unit: str = Field(..., min_length=1, max_length=50, description="Unit of measurement")
    unit_price: float = Field(..., ge=0, description="Price per unit")
    labor_cost: float = Field(default=0.0, ge=0, description="Labor cost per unit")
    material_cost: float = Field(default=0.0, ge=0, description="Material cost per unit")
    equipment_cost: float = Field(default=0.0, ge=0, description="Equipment cost per unit")
    markup_percentage: float = Field(default=0.0, ge=0, le=100, description="Markup percentage")
    is_active: bool = Field(default=True, description="Whether the cost code is active")
    notes: Optional[str] = Field(None, description="Additional notes")


class CostCodeCreate(CostCodeBase):
    """Schema for creating a new cost code."""

    @field_validator("code")
    @classmethod
    def validate_code_format(cls, v: str) -> str:
        """Validate cost code format."""
        if not v.strip():
            raise ValueError("Cost code cannot be empty")
        return v.upper().strip()


class CostCodeUpdate(BaseModel):
    """Schema for updating an existing cost code."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    unit: Optional[str] = Field(None, min_length=1, max_length=50)
    unit_price: Optional[float] = Field(None, ge=0)
    labor_cost: Optional[float] = Field(None, ge=0)
    material_cost: Optional[float] = Field(None, ge=0)
    equipment_cost: Optional[float] = Field(None, ge=0)
    markup_percentage: Optional[float] = Field(None, ge=0, le=100)
    is_active: Optional[bool] = None
    notes: Optional[str] = None


class CostCodeResponse(CostCodeBase):
    """Schema for cost code response."""

    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}


class CostCodeList(BaseModel):
    """Schema for paginated cost code list."""

    items: list[CostCodeResponse]
    total: int
    page: int
    page_size: int
    pages: int
