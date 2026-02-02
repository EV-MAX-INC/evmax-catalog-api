"""
Tests for the EV MAX Catalog API.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import ChargingType

client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_root_endpoint(self):
        """Test root endpoint returns health status."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "endpoints" in data
    
    def test_health_check(self):
        """Test detailed health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["cost_codes_loaded"] >= 83
        assert "configuration" in data


class TestCostCodeEndpoints:
    """Test cost code endpoints."""
    
    def test_list_all_cost_codes(self):
        """Test listing all cost codes."""
        response = client.get("/cost-codes/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 83
        assert all("code" in item for item in data)
        assert all("category" in item for item in data)
    
    def test_list_cost_codes_by_category(self):
        """Test filtering cost codes by category."""
        response = client.get("/cost-codes/?category=Concrete")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 10
        assert all(item["category"] == "Concrete" for item in data)
    
    def test_get_cost_code_by_code(self):
        """Test getting a specific cost code."""
        response = client.get("/cost-codes/CONC-001")
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "CONC-001"
        assert data["category"] == "Concrete"
        assert data["unit_cost"] > 0
    
    def test_get_nonexistent_cost_code(self):
        """Test getting a nonexistent cost code returns 404."""
        response = client.get("/cost-codes/INVALID-999")
        assert response.status_code == 404
    
    def test_search_cost_codes(self):
        """Test searching cost codes."""
        response = client.get("/cost-codes/search?q=concrete")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert any("concrete" in item["description"].lower() for item in data)
    
    def test_list_categories(self):
        """Test listing all categories."""
        response = client.get("/cost-codes/categories")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 9
        assert "Concrete" in data
        assert "Labor" in data


class TestBOMEndpoints:
    """Test BOM generation endpoints."""
    
    def test_generate_l2_bom(self):
        """Test generating BOM for L2 charging."""
        project_spec = {
            "project_name": "Test L2 Project",
            "charging_type": "L2",
            "num_ports": 4,
            "excavation_length": 150
        }
        response = client.post("/bom/generate", json=project_spec)
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert all("cost_code" in item for item in data)
        assert all("quantity" in item for item in data)
        assert all("subtotal" in item for item in data)
    
    def test_generate_dc_fast_bom(self):
        """Test generating BOM for DC Fast charging."""
        project_spec = {
            "project_name": "Test DC Fast Project",
            "charging_type": "DC_FAST",
            "num_ports": 2,
            "excavation_length": 200
        }
        response = client.post("/bom/generate", json=project_spec)
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        # DC Fast should include expensive equipment
        assert any(item["unit_cost"] > 30000 for item in data)


class TestBidCalculationEndpoints:
    """Test bid calculation endpoints."""
    
    def test_calculate_l2_bid(self):
        """Test calculating bid for L2 charging."""
        project_spec = {
            "project_name": "Test L2 Bid",
            "charging_type": "L2",
            "num_ports": 4,
            "excavation_length": 150
        }
        response = client.post("/bids/calculate", json=project_spec)
        assert response.status_code == 200
        data = response.json()
        
        # Verify all required fields
        assert data["project_name"] == "Test L2 Bid"
        assert data["charging_type"] == "L2"
        assert data["num_ports"] == 4
        assert data["material_cost"] > 0
        assert data["labor_cost"] > 0
        assert data["subtotal"] > 0
        assert data["total_cost"] > data["subtotal"]
        assert data["cost_per_port"] == data["total_cost"] / 4
        
        # Verify markups are applied
        assert data["material_markup"] == 0.10
        assert data["overhead_rate"] == 0.18
        assert data["excavation_contingency"] == 0.15
        assert data["profit_margin"] == 0.27
    
    def test_calculate_dc_fast_bid(self):
        """Test calculating bid for DC Fast charging."""
        project_spec = {
            "project_name": "Test DC Fast Bid",
            "charging_type": "DC_FAST",
            "num_ports": 2,
            "excavation_length": 200
        }
        response = client.post("/bids/calculate", json=project_spec)
        assert response.status_code == 200
        data = response.json()
        
        # DC Fast should be more expensive
        assert data["total_cost"] > 50000
        assert data["cost_per_port"] > 25000


class TestROIEndpoints:
    """Test ROI analysis endpoints."""
    
    def test_analyze_roi_default_parameters(self):
        """Test ROI analysis with default parameters."""
        project_spec = {
            "project_name": "Test ROI Project",
            "charging_type": "L2",
            "num_ports": 4,
            "excavation_length": 150
        }
        response = client.post("/roi/analyze", json=project_spec)
        assert response.status_code == 200
        data = response.json()
        
        # Verify all required fields
        assert data["project_name"] == "Test ROI Project"
        assert data["initial_investment"] > 0
        assert data["total_annual_revenue"] > 0
        assert data["annual_net_income"] > 0
        assert data["payback_period_years"] > 0
        assert data["ten_year_net_profit"] != 0
    
    def test_analyze_roi_custom_parameters(self):
        """Test ROI analysis with custom revenue parameters."""
        project_spec = {
            "project_name": "Test Custom ROI",
            "charging_type": "L2",
            "num_ports": 4,
            "excavation_length": 150
        }
        response = client.post(
            "/roi/analyze?annual_revenue_per_port=6000&annual_operating_cost_per_port=1000",
            json=project_spec
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify custom parameters are used
        assert data["annual_revenue_per_port"] == 6000
        assert data["total_annual_revenue"] == 24000  # 6000 * 4 ports


class TestBenchmarkEndpoints:
    """Test benchmark comparison endpoints."""
    
    def test_compare_benchmarks_l2(self):
        """Test benchmark comparison for L2 charging."""
        project_spec = {
            "project_name": "Test Benchmark L2",
            "charging_type": "L2",
            "num_ports": 4,
            "excavation_length": 150
        }
        response = client.post("/benchmarks/compare", json=project_spec)
        assert response.status_code == 200
        data = response.json()
        
        # Verify comparison data
        assert data["project_name"] == "Test Benchmark L2"
        assert data["num_ports"] == 4
        assert data["evmax_cost_per_port"] > 0
        assert data["keystone_cost_per_port"] > 0
        assert data["gges_cost_per_port"] > 0
        assert "evmax_vs_keystone_savings" in data
        assert "evmax_vs_gges_savings" in data
    
    def test_compare_benchmarks_dc_fast(self):
        """Test benchmark comparison for DC Fast charging."""
        project_spec = {
            "project_name": "Test Benchmark DC",
            "charging_type": "DC_FAST",
            "num_ports": 2,
            "excavation_length": 200
        }
        response = client.post("/benchmarks/compare", json=project_spec)
        assert response.status_code == 200
        data = response.json()
        
        # DC Fast benchmarks should be higher
        assert data["keystone_cost_per_port"] > 40000
        assert data["gges_cost_per_port"] > 40000
    
    def test_get_industry_averages(self):
        """Test getting industry average costs."""
        response = client.get("/benchmarks/industry-averages")
        assert response.status_code == 200
        data = response.json()
        
        # Verify all benchmark data is present
        assert "l2_cost_per_port_keystone" in data
        assert "l2_cost_per_port_gges" in data
        assert "dc_fast_cost_per_port_keystone" in data
        assert "dc_fast_cost_per_port_gges" in data
        assert data["industry_average_l2"] > 0
        assert data["industry_average_dc_fast"] > 0


class TestDataValidation:
    """Test data validation and error handling."""
    
    def test_invalid_charging_type(self):
        """Test that invalid charging type is rejected."""
        project_spec = {
            "project_name": "Invalid Project",
            "charging_type": "INVALID_TYPE",
            "num_ports": 4
        }
        response = client.post("/bom/generate", json=project_spec)
        assert response.status_code == 422
    
    def test_zero_ports(self):
        """Test that zero ports is rejected."""
        project_spec = {
            "project_name": "Zero Ports",
            "charging_type": "L2",
            "num_ports": 0
        }
        response = client.post("/bom/generate", json=project_spec)
        assert response.status_code == 422
    
    def test_negative_excavation(self):
        """Test that negative excavation length is rejected."""
        project_spec = {
            "project_name": "Negative Excavation",
            "charging_type": "L2",
            "num_ports": 4,
            "excavation_length": -100
        }
        response = client.post("/bom/generate", json=project_spec)
        assert response.status_code == 422
