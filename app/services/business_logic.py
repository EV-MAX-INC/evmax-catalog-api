"""
Business logic services for bid calculations, BOM generation, and ROI analysis.
"""
from typing import List, Dict, Optional
from app.models import (
    BOMLineItem, ProjectSpecification, BidCalculation, ROIAnalysis,
    ChargingType, CostCode
)
from app.config import settings
from app.data.cost_codes import cost_code_db


class BOMService:
    """Service for generating Bill of Materials."""
    
    def generate_bom(self, project_spec: ProjectSpecification) -> List[BOMLineItem]:
        """Generate BOM based on project specifications."""
        bom_items = []
        
        if project_spec.charging_type == ChargingType.L2:
            bom_items = self._generate_l2_bom(project_spec)
        elif project_spec.charging_type == ChargingType.DC_FAST:
            bom_items = self._generate_dc_fast_bom(project_spec)
        
        return bom_items
    
    def _generate_l2_bom(self, spec: ProjectSpecification) -> List[BOMLineItem]:
        """Generate BOM for L2 charging installation."""
        items = []
        
        # Charging equipment
        charger = cost_code_db.get_by_code("EQUIP-001")
        items.append(BOMLineItem(
            cost_code=charger.code,
            description=charger.description,
            quantity=spec.num_ports,
            unit=charger.unit,
            unit_cost=charger.unit_cost,
            subtotal=charger.unit_cost * spec.num_ports
        ))
        
        # Electrical panel (one per 4 ports)
        panel_count = max(1, (spec.num_ports + 3) // 4)
        panel = cost_code_db.get_by_code("EQUIP-006")
        items.append(BOMLineItem(
            cost_code=panel.code,
            description=panel.description,
            quantity=panel_count,
            unit=panel.unit,
            unit_cost=panel.unit_cost,
            subtotal=panel.unit_cost * panel_count
        ))
        
        # Concrete pad (20 SF per port)
        concrete_sf = 20 * spec.num_ports
        concrete = cost_code_db.get_by_code("CONC-001")
        items.append(BOMLineItem(
            cost_code=concrete.code,
            description=concrete.description,
            quantity=concrete_sf,
            unit=concrete.unit,
            unit_cost=concrete.unit_cost,
            subtotal=concrete.unit_cost * concrete_sf
        ))
        
        # Conduit (based on excavation length or default)
        conduit_length = spec.excavation_length or (50 * spec.num_ports)
        conduit = cost_code_db.get_by_code("COND-002")
        items.append(BOMLineItem(
            cost_code=conduit.code,
            description=conduit.description,
            quantity=conduit_length,
            unit=conduit.unit,
            unit_cost=conduit.unit_cost,
            subtotal=conduit.unit_cost * conduit_length
        ))
        
        # Wire (#6 AWG, 3 conductors per port)
        wire_length = conduit_length * 3
        wire = cost_code_db.get_by_code("WIRE-001")
        items.append(BOMLineItem(
            cost_code=wire.code,
            description=wire.description,
            quantity=wire_length,
            unit=wire.unit,
            unit_cost=wire.unit_cost,
            subtotal=wire.unit_cost * wire_length
        ))
        
        # Excavation
        excavation = cost_code_db.get_by_code("SITE-001")
        items.append(BOMLineItem(
            cost_code=excavation.code,
            description=excavation.description,
            quantity=conduit_length,
            unit=excavation.unit,
            unit_cost=excavation.unit_cost,
            subtotal=excavation.unit_cost * conduit_length
        ))
        
        # Grounding (one per port)
        ground_rod = cost_code_db.get_by_code("GRND-001")
        items.append(BOMLineItem(
            cost_code=ground_rod.code,
            description=ground_rod.description,
            quantity=spec.num_ports,
            unit=ground_rod.unit,
            unit_cost=ground_rod.unit_cost,
            subtotal=ground_rod.unit_cost * spec.num_ports
        ))
        
        # Safety bollards (2 per port)
        bollard_count = spec.num_ports * 2
        bollard = cost_code_db.get_by_code("SAFE-001")
        items.append(BOMLineItem(
            cost_code=bollard.code,
            description=bollard.description,
            quantity=bollard_count,
            unit=bollard.unit,
            unit_cost=bollard.unit_cost,
            subtotal=bollard.unit_cost * bollard_count
        ))
        
        # Labor (estimated hours)
        labor_hours = 16 * spec.num_ports
        labor = cost_code_db.get_by_code("LABOR-001")
        items.append(BOMLineItem(
            cost_code=labor.code,
            description=labor.description,
            quantity=labor_hours,
            unit=labor.unit,
            unit_cost=labor.unit_cost,
            subtotal=labor.unit_cost * labor_hours
        ))
        
        # Restoration (asphalt patching)
        restoration_sf = conduit_length * 3
        restoration = cost_code_db.get_by_code("REST-001")
        items.append(BOMLineItem(
            cost_code=restoration.code,
            description=restoration.description,
            quantity=restoration_sf,
            unit=restoration.unit,
            unit_cost=restoration.unit_cost,
            subtotal=restoration.unit_cost * restoration_sf
        ))
        
        return items
    
    def _generate_dc_fast_bom(self, spec: ProjectSpecification) -> List[BOMLineItem]:
        """Generate BOM for DC Fast charging installation."""
        items = []
        
        # DC Fast charger
        charger = cost_code_db.get_by_code("EQUIP-003")
        items.append(BOMLineItem(
            cost_code=charger.code,
            description=charger.description,
            quantity=spec.num_ports,
            unit=charger.unit,
            unit_cost=charger.unit_cost,
            subtotal=charger.unit_cost * spec.num_ports
        ))
        
        # Transformer (one per 2 ports)
        transformer_count = max(1, (spec.num_ports + 1) // 2)
        transformer = cost_code_db.get_by_code("EQUIP-008")
        items.append(BOMLineItem(
            cost_code=transformer.code,
            description=transformer.description,
            quantity=transformer_count,
            unit=transformer.unit,
            unit_cost=transformer.unit_cost,
            subtotal=transformer.unit_cost * transformer_count
        ))
        
        # Reinforced concrete pad (larger for DC)
        concrete_sf = 40 * spec.num_ports
        concrete = cost_code_db.get_by_code("CONC-008")
        items.append(BOMLineItem(
            cost_code=concrete.code,
            description=concrete.description,
            quantity=concrete_sf,
            unit=concrete.unit,
            unit_cost=concrete.unit_cost,
            subtotal=concrete.unit_cost * concrete_sf
        ))
        
        # Heavy conduit
        conduit_length = spec.excavation_length or (75 * spec.num_ports)
        conduit = cost_code_db.get_by_code("COND-007")
        items.append(BOMLineItem(
            cost_code=conduit.code,
            description=conduit.description,
            quantity=conduit_length,
            unit=conduit.unit,
            unit_cost=conduit.unit_cost,
            subtotal=conduit.unit_cost * conduit_length
        ))
        
        # Heavy wire (500 kcmil)
        wire_length = conduit_length * 3
        wire = cost_code_db.get_by_code("WIRE-010")
        items.append(BOMLineItem(
            cost_code=wire.code,
            description=wire.description,
            quantity=wire_length,
            unit=wire.unit,
            unit_cost=wire.unit_cost,
            subtotal=wire.unit_cost * wire_length
        ))
        
        # Excavation (deeper for DC)
        excavation = cost_code_db.get_by_code("SITE-001")
        items.append(BOMLineItem(
            cost_code=excavation.code,
            description=excavation.description,
            quantity=conduit_length,
            unit=excavation.unit,
            unit_cost=excavation.unit_cost * 1.5,  # 50% more for deeper trenches
            subtotal=excavation.unit_cost * conduit_length * 1.5
        ))
        
        # Advanced grounding
        ground_rod = cost_code_db.get_by_code("GRND-002")
        items.append(BOMLineItem(
            cost_code=ground_rod.code,
            description=ground_rod.description,
            quantity=spec.num_ports * 2,  # More grounding for DC
            unit=ground_rod.unit,
            unit_cost=ground_rod.unit_cost,
            subtotal=ground_rod.unit_cost * spec.num_ports * 2
        ))
        
        # Safety equipment
        bollard_count = spec.num_ports * 3
        bollard = cost_code_db.get_by_code("SAFE-001")
        items.append(BOMLineItem(
            cost_code=bollard.code,
            description=bollard.description,
            quantity=bollard_count,
            unit=bollard.unit,
            unit_cost=bollard.unit_cost,
            subtotal=bollard.unit_cost * bollard_count
        ))
        
        # Specialized labor (more hours for DC)
        labor_hours = 40 * spec.num_ports
        labor = cost_code_db.get_by_code("LABOR-002")  # Master electrician
        items.append(BOMLineItem(
            cost_code=labor.code,
            description=labor.description,
            quantity=labor_hours,
            unit=labor.unit,
            unit_cost=labor.unit_cost,
            subtotal=labor.unit_cost * labor_hours
        ))
        
        # Restoration
        restoration_sf = conduit_length * 4
        restoration = cost_code_db.get_by_code("REST-002")
        items.append(BOMLineItem(
            cost_code=restoration.code,
            description=restoration.description,
            quantity=restoration_sf,
            unit=restoration.unit,
            unit_cost=restoration.unit_cost,
            subtotal=restoration.unit_cost * restoration_sf
        ))
        
        return items


class BidCalculationService:
    """Service for calculating complete bids with markups and margins."""
    
    def __init__(self):
        self.bom_service = BOMService()
    
    def calculate_bid(self, project_spec: ProjectSpecification) -> BidCalculation:
        """Calculate complete bid with all markups and margins."""
        # Generate BOM
        bom_items = self.bom_service.generate_bom(project_spec)
        
        # Calculate base costs
        material_cost = 0.0
        labor_cost = 0.0
        
        for item in bom_items:
            # Get original cost code to split material/labor
            cost_code = cost_code_db.get_by_code(item.cost_code)
            if cost_code:
                if cost_code.material_cost:
                    material_cost += cost_code.material_cost * item.quantity
                if cost_code.labor_cost:
                    labor_cost += cost_code.labor_cost * item.quantity
            else:
                # If we can't split, assume half-half
                material_cost += item.subtotal * 0.5
                labor_cost += item.subtotal * 0.5
        
        subtotal = material_cost + labor_cost
        
        # Apply markups and margins
        material_markup_amount = material_cost * settings.material_markup
        overhead_amount = subtotal * settings.overhead_rate
        excavation_contingency_amount = subtotal * settings.ga_excavation_contingency
        
        # Calculate profit on top of everything
        cost_before_profit = subtotal + material_markup_amount + overhead_amount + excavation_contingency_amount
        profit_amount = cost_before_profit * settings.target_profit_margin
        
        total_cost = cost_before_profit + profit_amount
        cost_per_port = total_cost / project_spec.num_ports
        
        return BidCalculation(
            project_name=project_spec.project_name,
            charging_type=project_spec.charging_type,
            num_ports=project_spec.num_ports,
            material_cost=material_cost,
            labor_cost=labor_cost,
            subtotal=subtotal,
            material_markup=settings.material_markup,
            material_markup_amount=material_markup_amount,
            overhead_rate=settings.overhead_rate,
            overhead_amount=overhead_amount,
            excavation_contingency=settings.ga_excavation_contingency,
            excavation_contingency_amount=excavation_contingency_amount,
            profit_margin=settings.target_profit_margin,
            profit_amount=profit_amount,
            total_cost=total_cost,
            cost_per_port=cost_per_port
        )


class ROIAnalysisService:
    """Service for calculating ROI and financial projections."""
    
    def calculate_roi(
        self,
        bid: BidCalculation,
        annual_revenue_per_port: float = 5000.0,
        annual_operating_cost_per_port: float = 800.0
    ) -> ROIAnalysis:
        """
        Calculate ROI with 10-year projections.
        
        Args:
            bid: The bid calculation results
            annual_revenue_per_port: Expected annual revenue per port (default: $5,000)
            annual_operating_cost_per_port: Annual operating cost per port (default: $800)
        """
        initial_investment = bid.total_cost
        total_annual_revenue = annual_revenue_per_port * bid.num_ports
        annual_operating_cost = annual_operating_cost_per_port * bid.num_ports
        annual_net_income = total_annual_revenue - annual_operating_cost
        
        # Calculate payback period
        if annual_net_income > 0:
            payback_period_years = initial_investment / annual_net_income
        else:
            payback_period_years = float('inf')
        
        # Calculate ROI percentages
        roi_percentage = (annual_net_income / initial_investment) * 100 if initial_investment > 0 else 0
        
        # 10-year projections
        ten_year_revenue = total_annual_revenue * settings.roi_analysis_years
        ten_year_operating_cost = annual_operating_cost * settings.roi_analysis_years
        ten_year_net_profit = ten_year_revenue - ten_year_operating_cost - initial_investment
        ten_year_roi_percentage = (ten_year_net_profit / initial_investment) * 100 if initial_investment > 0 else 0
        
        return ROIAnalysis(
            project_name=bid.project_name,
            initial_investment=initial_investment,
            annual_revenue_per_port=annual_revenue_per_port,
            total_annual_revenue=total_annual_revenue,
            annual_operating_cost=annual_operating_cost,
            annual_net_income=annual_net_income,
            payback_period_years=payback_period_years,
            roi_percentage=roi_percentage,
            ten_year_net_profit=ten_year_net_profit,
            ten_year_roi_percentage=ten_year_roi_percentage
        )
