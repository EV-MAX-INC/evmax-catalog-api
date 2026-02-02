"""
Tests for cost code data.
"""
import pytest
from app.data.cost_codes import cost_code_db, CostCodeDatabase
from app.models import CostCategory


class TestCostCodeDatabase:
    """Test cost code database functionality."""
    
    def test_database_initialization(self):
        """Test database is properly initialized."""
        assert len(cost_code_db.get_all()) >= 83
    
    def test_all_categories_present(self):
        """Test all 9 categories have cost codes."""
        for category in CostCategory:
            codes = cost_code_db.get_by_category(category)
            assert len(codes) > 0, f"Category {category} has no cost codes"
    
    def test_get_by_code(self):
        """Test retrieving cost codes by code."""
        # Test known codes
        conc_001 = cost_code_db.get_by_code("CONC-001")
        assert conc_001 is not None
        assert conc_001.code == "CONC-001"
        assert conc_001.category == CostCategory.CONCRETE
        
        # Test non-existent code
        invalid = cost_code_db.get_by_code("INVALID-999")
        assert invalid is None
    
    def test_get_by_category(self):
        """Test retrieving cost codes by category."""
        concrete_codes = cost_code_db.get_by_category(CostCategory.CONCRETE)
        assert len(concrete_codes) >= 10
        assert all(code.category == CostCategory.CONCRETE for code in concrete_codes)
        
        labor_codes = cost_code_db.get_by_category(CostCategory.LABOR)
        assert len(labor_codes) >= 10
        assert all(code.category == CostCategory.LABOR for code in labor_codes)
    
    def test_search_functionality(self):
        """Test search functionality."""
        # Search by description
        concrete_results = cost_code_db.search("concrete")
        assert len(concrete_results) > 0
        
        # Search by code
        conc_results = cost_code_db.search("CONC")
        assert len(conc_results) >= 10
        # Verify at least most results contain CONC (may also match descriptions)
        conc_codes = [code for code in conc_results if "CONC" in code.code]
        assert len(conc_codes) >= 10
        
        # Search with no results
        no_results = cost_code_db.search("nonexistentterm123")
        assert len(no_results) == 0
    
    def test_cost_code_structure(self):
        """Test that all cost codes have required fields."""
        for code in cost_code_db.get_all():
            assert code.code is not None
            assert code.category is not None
            assert code.description is not None
            assert code.unit is not None
            assert code.unit_cost > 0
    
    def test_category_counts(self):
        """Test expected number of codes per category."""
        # Verify we have the expected minimum codes per category
        expected_minimums = {
            CostCategory.CONCRETE: 10,
            CostCategory.CONDUIT: 15,
            CostCategory.WIRE: 12,
            CostCategory.LABOR: 10,
            CostCategory.EQUIPMENT: 15,
            CostCategory.SAFETY: 8,
            CostCategory.SITE: 10,
            CostCategory.RESTORATION: 8,
            CostCategory.GROUNDING: 7
        }
        
        for category, min_count in expected_minimums.items():
            codes = cost_code_db.get_by_category(category)
            assert len(codes) >= min_count, f"Category {category} has only {len(codes)} codes, expected at least {min_count}"
    
    def test_specific_equipment_codes(self):
        """Test that specific equipment codes exist."""
        # L2 chargers
        l2_7kw = cost_code_db.get_by_code("EQUIP-001")
        assert l2_7kw is not None
        assert "7.2 kW" in l2_7kw.description or "L2" in l2_7kw.description
        
        # DC Fast chargers
        dc_50kw = cost_code_db.get_by_code("EQUIP-003")
        assert dc_50kw is not None
        assert "50 kW" in dc_50kw.description or "DC" in dc_50kw.description
    
    def test_material_labor_split(self):
        """Test that cost codes with material/labor split are consistent."""
        for code in cost_code_db.get_all():
            if code.material_cost is not None and code.labor_cost is not None:
                # Material + labor should approximately equal unit cost
                total = code.material_cost + code.labor_cost
                # Allow small rounding differences
                assert abs(total - code.unit_cost) < 0.02
