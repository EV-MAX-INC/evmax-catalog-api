"""
Data models for the EV MAX Catalog API.
"""
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class CostCategory(str, Enum):
    """Cost code categories."""
    CONCRETE = "Concrete"
    CONDUIT = "Conduit"
    WIRE = "Wire"
    LABOR = "Labor"
    EQUIPMENT = "Equipment"
    SAFETY = "Safety"
    SITE = "Site"
    RESTORATION = "Restoration"
    GROUNDING = "Grounding"


class ChargingType(str, Enum):
    """Types of charging infrastructure."""
    L2 = "L2"
    DC_FAST = "DC_FAST"


class CostCode(BaseModel):
    """Individual cost code item."""
    code: str = Field(..., description="Unique cost code (e.g., CONC-001)")
    category: CostCategory = Field(..., description="Cost category")
    description: str = Field(..., description="Item description")
    unit: str = Field(..., description="Unit of measurement (e.g., LF, EA, CY)")
    unit_cost: float = Field(..., description="Base unit cost in dollars", ge=0)
    material_cost: Optional[float] = Field(None, description="Material cost component", ge=0)
    labor_cost: Optional[float] = Field(None, description="Labor cost component", ge=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": "CONC-001",
                "category": "Concrete",
                "description": "4-inch concrete pad",
                "unit": "SF",
                "unit_cost": 8.50,
                "material_cost": 4.25,
                "labor_cost": 4.25
            }
        }


class BOMLineItem(BaseModel):
    """Bill of Materials line item."""
    cost_code: str = Field(..., description="Cost code reference")
    description: str
    quantity: float = Field(..., description="Quantity needed", gt=0)
    unit: str
    unit_cost: float = Field(..., ge=0)
    subtotal: float = Field(..., ge=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "cost_code": "CONC-001",
                "description": "4-inch concrete pad",
                "quantity": 100,
                "unit": "SF",
                "unit_cost": 8.50,
                "subtotal": 850.00
            }
        }


class ProjectSpecification(BaseModel):
    """Project specifications for bid generation."""
    project_name: str = Field(..., description="Project identifier")
    charging_type: ChargingType
    num_ports: int = Field(..., description="Number of charging ports", gt=0)
    site_conditions: Optional[str] = Field(None, description="Special site conditions")
    excavation_length: Optional[float] = Field(None, description="Excavation length in feet", ge=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "project_name": "Downtown Station A",
                "charging_type": "L2",
                "num_ports": 4,
                "site_conditions": "Standard urban installation",
                "excavation_length": 150
            }
        }


class BidCalculation(BaseModel):
    """Complete bid calculation results."""
    project_name: str
    charging_type: ChargingType
    num_ports: int
    
    # Cost breakdown
    material_cost: float = Field(..., ge=0)
    labor_cost: float = Field(..., ge=0)
    subtotal: float = Field(..., ge=0)
    
    # Markups and margins
    material_markup: float = Field(..., ge=0)
    material_markup_amount: float = Field(..., ge=0)
    overhead_rate: float = Field(..., ge=0)
    overhead_amount: float = Field(..., ge=0)
    excavation_contingency: float = Field(..., ge=0)
    excavation_contingency_amount: float = Field(..., ge=0)
    profit_margin: float = Field(..., ge=0)
    profit_amount: float = Field(..., ge=0)
    
    # Totals
    total_cost: float = Field(..., ge=0)
    cost_per_port: float = Field(..., ge=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "project_name": "Downtown Station A",
                "charging_type": "L2",
                "num_ports": 4,
                "material_cost": 15000,
                "labor_cost": 10000,
                "subtotal": 25000,
                "material_markup": 0.10,
                "material_markup_amount": 1500,
                "overhead_rate": 0.18,
                "overhead_amount": 4500,
                "excavation_contingency": 0.15,
                "excavation_contingency_amount": 3750,
                "profit_margin": 0.27,
                "profit_amount": 6750,
                "total_cost": 41500,
                "cost_per_port": 10375
            }
        }


class ROIAnalysis(BaseModel):
    """ROI and financial projection analysis."""
    project_name: str
    initial_investment: float = Field(..., ge=0)
    
    # Revenue assumptions
    annual_revenue_per_port: float = Field(..., ge=0)
    total_annual_revenue: float = Field(..., ge=0)
    
    # Operating costs
    annual_operating_cost: float = Field(..., ge=0)
    annual_net_income: float = Field(..., ge=0)
    
    # ROI metrics
    payback_period_years: float = Field(..., ge=0)
    roi_percentage: float
    ten_year_net_profit: float
    ten_year_roi_percentage: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "project_name": "Downtown Station A",
                "initial_investment": 41500,
                "annual_revenue_per_port": 5000,
                "total_annual_revenue": 20000,
                "annual_operating_cost": 4000,
                "annual_net_income": 16000,
                "payback_period_years": 2.59,
                "roi_percentage": 38.55,
                "ten_year_net_profit": 118500,
                "ten_year_roi_percentage": 285.54
            }
        }
