"""Bid Pydantic schemas for API validation."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class BidLineItem(BaseModel):
    """Schema for bid line item."""

    cost_code_id: int
    cost_code: str
    description: str
    quantity: float = Field(..., gt=0)
    unit_price: float = Field(..., ge=0)
    total: float = Field(..., ge=0)


class BidBase(BaseModel):
    """Base bid schema with common fields."""

    project_name: str = Field(..., min_length=1, max_length=255)
    client_name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    tax_rate: float = Field(default=0.0, ge=0, le=100)
    estimated_revenue: Optional[float] = Field(None, ge=0)
    estimated_cost: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None
    valid_until: Optional[datetime] = None


class BidCreate(BidBase):
    """Schema for creating a new bid."""

    line_items: List[BidLineItem] = Field(default_factory=list)


class BidUpdate(BaseModel):
    """Schema for updating an existing bid."""

    project_name: Optional[str] = Field(None, min_length=1, max_length=255)
    client_name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(draft|submitted|accepted|rejected)$")
    tax_rate: Optional[float] = Field(None, ge=0, le=100)
    estimated_revenue: Optional[float] = Field(None, ge=0)
    estimated_cost: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None
    valid_until: Optional[datetime] = None
    line_items: Optional[List[BidLineItem]] = None


class BidResponse(BidBase):
    """Schema for bid response."""

    id: int
    bid_number: str
    status: str
    subtotal: float
    tax_amount: float
    total_amount: float
    estimated_roi_percentage: Optional[float]
    estimated_payback_months: Optional[int]
    line_items: List[Dict[str, Any]]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}


class BidList(BaseModel):
    """Schema for paginated bid list."""

    items: List[BidResponse]
    total: int
    page: int
    page_size: int
    pages: int


class BidCalculateRequest(BaseModel):
    """Schema for bid calculation request."""

    line_items: List[Dict[str, Any]] = Field(..., min_length=1)
    tax_rate: float = Field(default=0.0, ge=0, le=100)


class BidCalculateResponse(BaseModel):
    """Schema for bid calculation response."""

    line_items: List[Dict[str, Any]]
    subtotal: float
    tax_amount: float
    total_amount: float


class ROIAnalysisRequest(BaseModel):
    """Schema for ROI analysis request."""

    estimated_revenue: float = Field(..., gt=0)
    estimated_cost: float = Field(..., gt=0)
    project_duration_months: int = Field(..., gt=0)


class ROIAnalysisResponse(BaseModel):
    """Schema for ROI analysis response."""

    roi_percentage: float
    profit: float
    payback_months: int
    estimated_revenue: float
    estimated_cost: float
    net_present_value: Optional[float] = None
