"""
Unit tests for business logic services.
"""
import pytest
from app.models import ProjectSpecification, ChargingType
from app.services import BOMService, BidCalculationService, ROIAnalysisService
from app.config import settings


class TestBOMService:
    """Test BOM generation service."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.bom_service = BOMService()
    
    def test_generate_l2_bom(self):
        """Test generating L2 BOM."""
        spec = ProjectSpecification(
            project_name="Test L2",
            charging_type=ChargingType.L2,
            num_ports=4,
            excavation_length=150
        )
        bom = self.bom_service.generate_bom(spec)
        
        assert len(bom) > 0
        assert all(item.quantity > 0 for item in bom)
        assert all(item.unit_cost > 0 for item in bom)
        assert all(item.subtotal > 0 for item in bom)
        
        # Verify key components are included
        codes = [item.cost_code for item in bom]
        assert any("EQUIP" in code for code in codes)  # Equipment
        assert any("CONC" in code for code in codes)   # Concrete
        assert any("COND" in code for code in codes)   # Conduit
        assert any("WIRE" in code for code in codes)   # Wire
        assert any("LABOR" in code for code in codes)  # Labor
    
    def test_generate_dc_fast_bom(self):
        """Test generating DC Fast BOM."""
        spec = ProjectSpecification(
            project_name="Test DC Fast",
            charging_type=ChargingType.DC_FAST,
            num_ports=2,
            excavation_length=200
        )
        bom = self.bom_service.generate_bom(spec)
        
        assert len(bom) > 0
        # DC Fast should have more expensive components
        assert any(item.unit_cost > 30000 for item in bom)
    
    def test_default_excavation_length(self):
        """Test BOM generation with default excavation length."""
        spec = ProjectSpecification(
            project_name="Test Default",
            charging_type=ChargingType.L2,
            num_ports=4
        )
        bom = self.bom_service.generate_bom(spec)
        
        # Should still generate valid BOM with calculated excavation
        assert len(bom) > 0


class TestBidCalculationService:
    """Test bid calculation service."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.bid_service = BidCalculationService()
    
    def test_calculate_bid_structure(self):
        """Test bid calculation returns correct structure."""
        spec = ProjectSpecification(
            project_name="Test Bid",
            charging_type=ChargingType.L2,
            num_ports=4,
            excavation_length=150
        )
        bid = self.bid_service.calculate_bid(spec)
        
        # Verify cost components
        assert bid.material_cost > 0
        assert bid.labor_cost > 0
        assert bid.subtotal == bid.material_cost + bid.labor_cost
        
        # Verify markups match configuration
        assert bid.material_markup == settings.material_markup
        assert bid.overhead_rate == settings.overhead_rate
        assert bid.excavation_contingency == settings.ga_excavation_contingency
        assert bid.profit_margin == settings.target_profit_margin
        
        # Verify markup amounts
        assert bid.material_markup_amount > 0
        assert bid.overhead_amount > 0
        assert bid.excavation_contingency_amount > 0
        assert bid.profit_amount > 0
        
        # Verify total calculation
        cost_before_profit = (
            bid.subtotal + 
            bid.material_markup_amount + 
            bid.overhead_amount + 
            bid.excavation_contingency_amount
        )
        expected_total = cost_before_profit + bid.profit_amount
        assert abs(bid.total_cost - expected_total) < 0.01
    
    def test_cost_per_port_calculation(self):
        """Test cost per port is correctly calculated."""
        spec = ProjectSpecification(
            project_name="Test Per Port",
            charging_type=ChargingType.L2,
            num_ports=5,
            excavation_length=150
        )
        bid = self.bid_service.calculate_bid(spec)
        
        expected_per_port = bid.total_cost / spec.num_ports
        assert abs(bid.cost_per_port - expected_per_port) < 0.01
    
    def test_dc_fast_more_expensive(self):
        """Test that DC Fast is more expensive than L2."""
        l2_spec = ProjectSpecification(
            project_name="L2 Compare",
            charging_type=ChargingType.L2,
            num_ports=2,
            excavation_length=150
        )
        dc_spec = ProjectSpecification(
            project_name="DC Compare",
            charging_type=ChargingType.DC_FAST,
            num_ports=2,
            excavation_length=150
        )
        
        l2_bid = self.bid_service.calculate_bid(l2_spec)
        dc_bid = self.bid_service.calculate_bid(dc_spec)
        
        assert dc_bid.total_cost > l2_bid.total_cost


class TestROIAnalysisService:
    """Test ROI analysis service."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.bid_service = BidCalculationService()
        self.roi_service = ROIAnalysisService()
    
    def test_calculate_roi_structure(self):
        """Test ROI calculation returns correct structure."""
        spec = ProjectSpecification(
            project_name="Test ROI",
            charging_type=ChargingType.L2,
            num_ports=4,
            excavation_length=150
        )
        bid = self.bid_service.calculate_bid(spec)
        roi = self.roi_service.calculate_roi(bid)
        
        # Verify basic structure
        assert roi.project_name == spec.project_name
        assert roi.initial_investment == bid.total_cost
        assert roi.annual_revenue_per_port > 0
        assert roi.total_annual_revenue > 0
        assert roi.annual_operating_cost >= 0
        assert roi.payback_period_years > 0
    
    def test_roi_calculations(self):
        """Test ROI percentage calculations."""
        spec = ProjectSpecification(
            project_name="Test ROI Calc",
            charging_type=ChargingType.L2,
            num_ports=4,
            excavation_length=150
        )
        bid = self.bid_service.calculate_bid(spec)
        roi = self.roi_service.calculate_roi(
            bid,
            annual_revenue_per_port=5000,
            annual_operating_cost_per_port=800
        )
        
        # Verify revenue calculations
        expected_annual_revenue = 5000 * spec.num_ports
        assert roi.total_annual_revenue == expected_annual_revenue
        
        expected_operating_cost = 800 * spec.num_ports
        assert roi.annual_operating_cost == expected_operating_cost
        
        expected_net_income = expected_annual_revenue - expected_operating_cost
        assert roi.annual_net_income == expected_net_income
        
        # Verify payback period
        expected_payback = bid.total_cost / expected_net_income
        assert abs(roi.payback_period_years - expected_payback) < 0.01
        
        # Verify annual ROI percentage
        expected_roi_pct = (expected_net_income / bid.total_cost) * 100
        assert abs(roi.roi_percentage - expected_roi_pct) < 0.01
    
    def test_ten_year_projections(self):
        """Test 10-year financial projections."""
        spec = ProjectSpecification(
            project_name="Test 10 Year",
            charging_type=ChargingType.L2,
            num_ports=4,
            excavation_length=150
        )
        bid = self.bid_service.calculate_bid(spec)
        roi = self.roi_service.calculate_roi(
            bid,
            annual_revenue_per_port=5000,
            annual_operating_cost_per_port=800
        )
        
        # Calculate expected 10-year values
        ten_year_revenue = roi.total_annual_revenue * settings.roi_analysis_years
        ten_year_operating = roi.annual_operating_cost * settings.roi_analysis_years
        expected_net_profit = ten_year_revenue - ten_year_operating - roi.initial_investment
        
        assert abs(roi.ten_year_net_profit - expected_net_profit) < 0.01
        
        # Verify 10-year ROI percentage
        expected_ten_year_roi = (expected_net_profit / roi.initial_investment) * 100
        assert abs(roi.ten_year_roi_percentage - expected_ten_year_roi) < 0.01
    
    def test_custom_revenue_parameters(self):
        """Test ROI with custom revenue parameters."""
        spec = ProjectSpecification(
            project_name="Test Custom",
            charging_type=ChargingType.L2,
            num_ports=4,
            excavation_length=150
        )
        bid = self.bid_service.calculate_bid(spec)
        roi = self.roi_service.calculate_roi(
            bid,
            annual_revenue_per_port=7500,
            annual_operating_cost_per_port=1200
        )
        
        assert roi.annual_revenue_per_port == 7500
        assert roi.total_annual_revenue == 7500 * 4
        assert roi.annual_operating_cost == 1200 * 4
