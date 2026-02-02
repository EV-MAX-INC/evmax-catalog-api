"""
Test configuration and fixtures.
"""
import pytest
from app.config import settings


@pytest.fixture
def sample_l2_project():
    """Sample L2 charging project specification."""
    return {
        "project_name": "Sample L2 Project",
        "charging_type": "L2",
        "num_ports": 4,
        "site_conditions": "Standard urban installation",
        "excavation_length": 150
    }


@pytest.fixture
def sample_dc_fast_project():
    """Sample DC Fast charging project specification."""
    return {
        "project_name": "Sample DC Fast Project",
        "charging_type": "DC_FAST",
        "num_ports": 2,
        "site_conditions": "Highway rest stop",
        "excavation_length": 200
    }


def test_settings_loaded():
    """Test that settings are properly loaded."""
    assert settings.material_markup == 0.10
    assert settings.overhead_rate == 0.18
    assert settings.ga_excavation_contingency == 0.15
    assert settings.target_profit_margin == 0.27
    assert settings.roi_analysis_years == 10
