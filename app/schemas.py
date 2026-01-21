from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class ProductBase(BaseModel):
    sku: str = Field(..., description="Unique product SKU")
    category: Optional[str] = Field(None, description="Product category")
    name: str = Field(..., description="Product name")
    base_cost: float = Field(..., gt=0, description="Base cost of the product")
    base_price: float = Field(..., gt=0, description="Base price of the product")
    pricing_tiers: Optional[Dict[str, Any]] = Field(None, description="Volume discount pricing tiers")
    material_specs: Optional[Dict[str, Any]] = Field(None, description="Material specifications")
    compliance_codes: Optional[str] = Field(None, description="Compliance codes (comma-separated)")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    sku: Optional[str] = None
    category: Optional[str] = None
    name: Optional[str] = None
    base_cost: Optional[float] = Field(None, gt=0)
    base_price: Optional[float] = Field(None, gt=0)
    pricing_tiers: Optional[Dict[str, Any]] = None
    material_specs: Optional[Dict[str, Any]] = None
    compliance_codes: Optional[str] = None


class Product(ProductBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class CostCodeBase(BaseModel):
    code: str = Field(..., description="Cost code identifier")
    description: Optional[str] = None
    category: Optional[str] = None
    base_rate: Optional[float] = Field(None, gt=0)


class CostCodeCreate(CostCodeBase):
    pass


class CostCodeUpdate(BaseModel):
    code: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    base_rate: Optional[float] = Field(None, gt=0)


class CostCode(CostCodeBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ComplianceStandardBase(BaseModel):
    code: str = Field(..., description="Compliance standard code")
    name: str = Field(..., description="Standard name")
    description: Optional[str] = None
    issuing_body: Optional[str] = None
    effective_date: Optional[datetime] = None


class ComplianceStandardCreate(ComplianceStandardBase):
    pass


class ComplianceStandardUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    issuing_body: Optional[str] = None
    effective_date: Optional[datetime] = None


class ComplianceStandard(ComplianceStandardBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class QuoteRequest(BaseModel):
    product_id: int = Field(..., description="Product ID")
    quantity: int = Field(..., gt=0, description="Quantity to quote")
    season: Optional[str] = Field(None, description="Season for seasonal pricing (winter, spring, summer, fall)")
    tier: Optional[str] = Field(None, description="Customer tier (standard, premium, enterprise)")


class QuoteResponse(BaseModel):
    product_id: int
    product_name: str
    sku: str
    quantity: int
    base_price: float
    unit_price: float
    volume_discount_percent: float
    seasonal_adjustment_percent: float
    tier_adjustment_percent: float
    subtotal: float
    total_price: float
    margin_percent: float
    margin_amount: float


class HealthCheck(BaseModel):
    status: str
    database: str
    timestamp: datetime
