"""Tests for contextual chain service and API."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.services.contextual_service import (
    ContextualLatheringEngine,
    ContextualChainNodeData,
)

# Create test database
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


@pytest.fixture
def db():
    """Create database session for testing."""
    session = TestingSessionLocal()
    yield session
    session.close()


def test_create_root_node(client):
    """Test creating a root node with no parents."""
    node_data = {
        "node_id": "root-node-1",
        "node_type": "cost_code",
        "parent_nodes": [],
        "metadata": {"description": "Root node"}
    }
    
    response = client.post("/api/v1/contextual-chains/nodes", json=node_data)
    assert response.status_code == 201
    data = response.json()
    assert data["node_id"] == "root-node-1"
    assert data["node_type"] == "cost_code"
    assert data["lathering_depth"] == 0
    assert data["parent_nodes"] == []


def test_create_child_node(client):
    """Test creating a child node with parent."""
    # Create root node first
    root_data = {
        "node_id": "root-2",
        "node_type": "cost_code",
        "parent_nodes": [],
        "metadata": {}
    }
    client.post("/api/v1/contextual-chains/nodes", json=root_data)
    
    # Create child node
    child_data = {
        "node_id": "child-2-1",
        "node_type": "bid",
        "parent_nodes": ["root-2"],
        "metadata": {"bid_number": "BID-001"}
    }
    
    response = client.post("/api/v1/contextual-chains/nodes", json=child_data)
    assert response.status_code == 201
    data = response.json()
    assert data["node_id"] == "child-2-1"
    assert data["lathering_depth"] == 1
    assert data["parent_nodes"] == ["root-2"]


def test_create_multi_level_chain(client):
    """Test creating a multi-level chain."""
    # Level 0: Root
    root_data = {
        "node_id": "root-3",
        "node_type": "cost_code",
        "parent_nodes": [],
        "metadata": {}
    }
    client.post("/api/v1/contextual-chains/nodes", json=root_data)
    
    # Level 1: Child
    child_data = {
        "node_id": "child-3-1",
        "node_type": "bid",
        "parent_nodes": ["root-3"],
        "metadata": {}
    }
    client.post("/api/v1/contextual-chains/nodes", json=child_data)
    
    # Level 2: Grandchild
    grandchild_data = {
        "node_id": "grandchild-3-1-1",
        "node_type": "roi_analysis",
        "parent_nodes": ["child-3-1"],
        "metadata": {}
    }
    
    response = client.post("/api/v1/contextual-chains/nodes", json=grandchild_data)
    assert response.status_code == 201
    data = response.json()
    assert data["lathering_depth"] == 2


def test_duplicate_node_id(client):
    """Test that duplicate node IDs are rejected."""
    node_data = {
        "node_id": "duplicate-node",
        "node_type": "cost_code",
        "parent_nodes": [],
        "metadata": {}
    }
    
    # First creation should succeed
    response = client.post("/api/v1/contextual-chains/nodes", json=node_data)
    assert response.status_code == 201
    
    # Second creation should fail
    response = client.post("/api/v1/contextual-chains/nodes", json=node_data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_circular_dependency_detection(client):
    """Test that circular dependencies are detected."""
    # Create chain: A -> B
    node_a = {
        "node_id": "node-a",
        "node_type": "cost_code",
        "parent_nodes": [],
        "metadata": {}
    }
    client.post("/api/v1/contextual-chains/nodes", json=node_a)
    
    node_b = {
        "node_id": "node-b",
        "node_type": "bid",
        "parent_nodes": ["node-a"],
        "metadata": {}
    }
    client.post("/api/v1/contextual-chains/nodes", json=node_b)
    
    # Try to create A with B as parent (would create cycle)
    # This should be prevented
    # Note: In current implementation, we can't modify existing nodes,
    # but we can test self-reference
    node_c = {
        "node_id": "node-c",
        "node_type": "cost_code",
        "parent_nodes": ["node-c"],  # Self-reference
        "metadata": {}
    }
    response = client.post("/api/v1/contextual-chains/nodes", json=node_c)
    assert response.status_code == 400
    assert "circular" in response.json()["detail"].lower()


def test_analyze_chain_node(client):
    """Test analyzing a node in the chain."""
    # Create a chain
    root = {
        "node_id": "analyze-root",
        "node_type": "cost_code",
        "parent_nodes": [],
        "metadata": {}
    }
    client.post("/api/v1/contextual-chains/nodes", json=root)
    
    child = {
        "node_id": "analyze-child",
        "node_type": "bid",
        "parent_nodes": ["analyze-root"],
        "metadata": {}
    }
    client.post("/api/v1/contextual-chains/nodes", json=child)
    
    # Analyze the child node
    response = client.get("/api/v1/contextual-chains/nodes/analyze-child/analysis")
    assert response.status_code == 200
    data = response.json()
    assert data["node_id"] == "analyze-child"
    assert data["lathering_depth"] == 1
    assert data["total_ancestors"] == 1
    assert "analyze-root" in data["heritage_lineage"]
    assert "chain_metrics" in data


def test_get_chain_snapshot(client):
    """Test getting a chain snapshot."""
    # Create a simple chain
    root = {
        "node_id": "snapshot-root",
        "node_type": "cost_code",
        "parent_nodes": [],
        "metadata": {}
    }
    client.post("/api/v1/contextual-chains/nodes", json=root)
    
    child1 = {
        "node_id": "snapshot-child-1",
        "node_type": "bid",
        "parent_nodes": ["snapshot-root"],
        "metadata": {}
    }
    client.post("/api/v1/contextual-chains/nodes", json=child1)
    
    child2 = {
        "node_id": "snapshot-child-2",
        "node_type": "bid",
        "parent_nodes": ["snapshot-root"],
        "metadata": {}
    }
    client.post("/api/v1/contextual-chains/nodes", json=child2)
    
    # Get snapshot
    response = client.get("/api/v1/contextual-chains/snapshots/snapshot-root")
    assert response.status_code == 200
    data = response.json()
    assert data["root_node"] == "snapshot-root"
    assert data["total_nodes"] == 3  # root + 2 children
    assert "node_tree" in data
    assert "snapshot_id" in data


def test_node_not_found(client):
    """Test that non-existent nodes return 404."""
    response = client.get("/api/v1/contextual-chains/nodes/non-existent/analysis")
    assert response.status_code == 404


def test_contextualize_bid(client):
    """Test contextualizing an existing bid."""
    # First create a cost code
    cost_code_data = {
        "code": "CC-CTX-001",
        "name": "Test Cost Code",
        "category": "Labor",
        "unit": "EA",
        "unit_price": 100.0,
    }
    cost_code_response = client.post("/api/v1/cost-codes", json=cost_code_data)
    cost_code = cost_code_response.json()
    cost_code_id = cost_code["id"]
    
    # Create a bid with line items
    bid_data = {
        "project_name": "Test Project",
        "client_name": "Test Customer",
        "line_items": [
            {
                "cost_code_id": cost_code_id,
                "cost_code": cost_code["code"],
                "description": cost_code["name"],
                "quantity": 5,
                "unit_price": 100.0,
                "total": 500.0
            }
        ]
    }
    bid_response = client.post("/api/v1/bids", json=bid_data)
    assert bid_response.status_code == 201
    bid_id = bid_response.json()["id"]
    
    # Contextualize the bid
    response = client.post(f"/api/v1/contextual-chains/bids/{bid_id}/contextualize")
    assert response.status_code == 201
    data = response.json()
    assert data["node_id"] == f"bid-{bid_id}"
    assert data["node_type"] == "bid"


def test_engine_heritage_lineage(db):
    """Test heritage lineage calculation using the engine directly."""
    engine = ContextualLatheringEngine(db)
    
    # Create a chain: root -> child1 -> grandchild
    root_node = ContextualChainNodeData(
        node_id="eng-root",
        node_type="cost_code",
        parent_nodes=[],
        metadata={}
    )
    engine.register_node(root_node)
    
    child_node = ContextualChainNodeData(
        node_id="eng-child",
        node_type="bid",
        parent_nodes=["eng-root"],
        metadata={}
    )
    engine.register_node(child_node)
    
    grandchild_node = ContextualChainNodeData(
        node_id="eng-grandchild",
        node_type="roi_analysis",
        parent_nodes=["eng-child"],
        metadata={}
    )
    engine.register_node(grandchild_node)
    
    # Check heritage lineage
    lineage = engine.get_heritage_lineage("eng-grandchild")
    assert len(lineage) == 2
    assert "eng-child" in lineage
    assert "eng-root" in lineage


def test_engine_chain_metrics(db):
    """Test chain metrics calculation."""
    engine = ContextualLatheringEngine(db)
    
    # Create a simple chain
    root = ContextualChainNodeData(
        node_id="metrics-root",
        node_type="cost_code",
        parent_nodes=[],
        metadata={"test": "value"}
    )
    engine.register_node(root)
    
    child = ContextualChainNodeData(
        node_id="metrics-child",
        node_type="bid",
        parent_nodes=["metrics-root"],
        metadata={}
    )
    engine.register_node(child)
    
    # Analyze metrics
    metrics = engine.analyze_chain_metrics("metrics-child")
    assert metrics["node_id"] == "metrics-child"
    assert metrics["lathering_depth"] == 1
    assert metrics["total_ancestors"] == 1
    assert metrics["is_root"] is False
    assert metrics["is_leaf"] is True


def test_multiple_parents(client):
    """Test node with multiple parent nodes."""
    # Create two root nodes
    root1 = {
        "node_id": "multi-root-1",
        "node_type": "cost_code",
        "parent_nodes": [],
        "metadata": {}
    }
    client.post("/api/v1/contextual-chains/nodes", json=root1)
    
    root2 = {
        "node_id": "multi-root-2",
        "node_type": "cost_code",
        "parent_nodes": [],
        "metadata": {}
    }
    client.post("/api/v1/contextual-chains/nodes", json=root2)
    
    # Create child with both parents
    child = {
        "node_id": "multi-child",
        "node_type": "bid",
        "parent_nodes": ["multi-root-1", "multi-root-2"],
        "metadata": {}
    }
    
    response = client.post("/api/v1/contextual-chains/nodes", json=child)
    assert response.status_code == 201
    data = response.json()
    assert data["lathering_depth"] == 1
    assert len(data["parent_nodes"]) == 2
    
    # Check heritage lineage
    analysis = client.get("/api/v1/contextual-chains/nodes/multi-child/analysis")
    assert analysis.status_code == 200
    analysis_data = analysis.json()
    assert analysis_data["total_ancestors"] == 2
