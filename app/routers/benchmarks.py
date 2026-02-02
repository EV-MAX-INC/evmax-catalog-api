"""
API router for benchmark comparisons.
"""
from typing import Dict
from fastapi import APIRouter
from pydantic import BaseModel
from app.models import ProjectSpecification, ChargingType

router = APIRouter(prefix="/benchmarks", tags=["Benchmarks"])


class BenchmarkComparison(BaseModel):
    """Benchmark comparison data."""
    project_name: str
    charging_type: ChargingType
    num_ports: int
    evmax_cost_per_port: float
    evmax_total_cost: float
    keystone_cost_per_port: float
    keystone_total_cost: float
    gges_cost_per_port: float
    gges_total_cost: float
    evmax_vs_keystone_savings: float
    evmax_vs_gges_savings: float
    evmax_vs_keystone_percentage: float
    evmax_vs_gges_percentage: float


@router.post("/compare", response_model=BenchmarkComparison)
async def compare_benchmarks(project_spec: ProjectSpecification):
    """
    Compare EV MAX pricing against industry benchmarks (Keystone and GGES).
    
    This provides a competitive analysis showing cost savings and
    percentage differences compared to other providers.
    
    Note: Benchmark prices are estimates based on industry averages.
    """
    from app.services import BidCalculationService
    
    bid_service = BidCalculationService()
    evmax_bid = bid_service.calculate_bid(project_spec)
    
    # Benchmark pricing (industry estimates)
    # These are typical competitor prices - adjust based on actual market data
    if project_spec.charging_type == ChargingType.L2:
        keystone_per_port = 12000.0
        gges_per_port = 13500.0
    else:  # DC_FAST
        keystone_per_port = 55000.0
        gges_per_port = 60000.0
    
    keystone_total = keystone_per_port * project_spec.num_ports
    gges_total = gges_per_port * project_spec.num_ports
    
    keystone_savings = keystone_total - evmax_bid.total_cost
    gges_savings = gges_total - evmax_bid.total_cost
    
    keystone_percentage = (keystone_savings / keystone_total * 100) if keystone_total > 0 else 0
    gges_percentage = (gges_savings / gges_total * 100) if gges_total > 0 else 0
    
    return BenchmarkComparison(
        project_name=project_spec.project_name,
        charging_type=project_spec.charging_type,
        num_ports=project_spec.num_ports,
        evmax_cost_per_port=evmax_bid.cost_per_port,
        evmax_total_cost=evmax_bid.total_cost,
        keystone_cost_per_port=keystone_per_port,
        keystone_total_cost=keystone_total,
        gges_cost_per_port=gges_per_port,
        gges_total_cost=gges_total,
        evmax_vs_keystone_savings=keystone_savings,
        evmax_vs_gges_savings=gges_savings,
        evmax_vs_keystone_percentage=keystone_percentage,
        evmax_vs_gges_percentage=gges_percentage
    )


@router.get("/industry-averages", response_model=Dict[str, float])
async def get_industry_averages():
    """
    Get industry average costs for different charging types.
    
    Provides benchmark data for comparison purposes.
    """
    return {
        "l2_cost_per_port_keystone": 12000.0,
        "l2_cost_per_port_gges": 13500.0,
        "dc_fast_cost_per_port_keystone": 55000.0,
        "dc_fast_cost_per_port_gges": 60000.0,
        "industry_average_l2": 12750.0,
        "industry_average_dc_fast": 57500.0
    }
