"""Basic API tests."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

# Create test database (in-memory for isolation with StaticPool to persist across requests)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables once at module level
Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    """Create test client."""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_create_cost_code(client):
    """Test creating a cost code."""
    cost_code_data = {
        "code": "CC001",
        "name": "Test Cost Code",
        "description": "Test description",
        "category": "Labor",
        "unit": "EA",
        "unit_price": 100.0,
        "labor_cost": 50.0,
        "material_cost": 30.0,
        "equipment_cost": 20.0,
        "markup_percentage": 10.0,
    }

    response = client.post("/api/v1/cost-codes", json=cost_code_data)
    assert response.status_code == 201
    data = response.json()
    assert data["code"] == "CC001"
    assert data["name"] == "Test Cost Code"
    assert data["unit_price"] == 100.0


def test_list_cost_codes(client):
    """Test listing cost codes."""
    # Create a cost code first
    cost_code_data = {
        "code": "CC002",
        "name": "Another Test Cost Code",
        "category": "Material",
        "unit": "LF",
        "unit_price": 50.0,
    }
    client.post("/api/v1/cost-codes", json=cost_code_data)

    # List cost codes
    response = client.get("/api/v1/cost-codes")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert len(data["items"]) > 0


def test_get_cost_code(client):
    """Test getting a specific cost code."""
    # Create a cost code first
    cost_code_data = {
        "code": "CC003",
        "name": "Specific Cost Code",
        "category": "Equipment",
        "unit": "HR",
        "unit_price": 75.0,
    }
    create_response = client.post("/api/v1/cost-codes", json=cost_code_data)
    cost_code_id = create_response.json()["id"]

    # Get the cost code
    response = client.get(f"/api/v1/cost-codes/{cost_code_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "CC003"


def test_create_bid(client):
    """Test creating a bid."""
    # Create a cost code first
    cost_code_data = {
        "code": "CC004",
        "name": "Bid Cost Code",
        "category": "Labor",
        "unit": "EA",
        "unit_price": 100.0,
    }
    cost_code_response = client.post("/api/v1/cost-codes", json=cost_code_data)
    cost_code_id = cost_code_response.json()["id"]

    # Create a bid
    bid_data = {
        "project_name": "Test Project",
        "client_name": "Test Client",
        "description": "Test bid description",
        "tax_rate": 8.5,
        "line_items": [
            {
                "cost_code_id": cost_code_id,
                "cost_code": "CC004",
                "description": "Bid Cost Code",
                "quantity": 10,
                "unit_price": 100.0,
                "total": 1000.0,
            }
        ],
    }

    response = client.post("/api/v1/bids", json=bid_data)
    assert response.status_code == 201
    data = response.json()
    assert data["project_name"] == "Test Project"
    assert data["subtotal"] > 0


def test_calculate_roi(client):
    """Test ROI calculation."""
    roi_data = {
        "estimated_revenue": 100000.0,
        "estimated_cost": 60000.0,
        "project_duration_months": 12,
    }

    response = client.post("/api/v1/analysis/roi", json=roi_data)
    assert response.status_code == 200
    data = response.json()
    assert "roi_percentage" in data
    assert "profit" in data
    assert data["roi_percentage"] > 0
