"""
Examples for using the Contextual Lathering String Heritage System.

This module demonstrates how to use the contextual chain functionality
to track heritage lineage, analyze chain metrics, and generate snapshots.
"""

import requests
import json
from typing import Dict, Any, List

# Base URL for the API
BASE_URL = "http://localhost:8000/api/v1"


def create_cost_code(code: str, name: str, unit_price: float) -> Dict[str, Any]:
    """
    Create a cost code and return the response.
    
    Args:
        code: Cost code identifier
        name: Cost code name
        unit_price: Unit price for the cost code
        
    Returns:
        API response dictionary
    """
    url = f"{BASE_URL}/cost-codes"
    payload = {
        "code": code,
        "name": name,
        "category": "Labor",
        "unit": "EA",
        "unit_price": unit_price,
    }
    
    response = requests.post(url, json=payload)
    return response.json()


def create_contextual_node(
    node_id: str,
    node_type: str,
    parent_nodes: List[str] = None,
    metadata: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Create a contextual chain node.
    
    Args:
        node_id: Unique node identifier
        node_type: Type of node (e.g., 'cost_code', 'bid')
        parent_nodes: List of parent node IDs
        metadata: Additional metadata
        
    Returns:
        API response dictionary
    """
    url = f"{BASE_URL}/contextual-chains/nodes"
    payload = {
        "node_id": node_id,
        "node_type": node_type,
        "parent_nodes": parent_nodes or [],
        "metadata": metadata or {}
    }
    
    response = requests.post(url, json=payload)
    return response.json()


def analyze_node(node_id: str) -> Dict[str, Any]:
    """
    Analyze a contextual chain node.
    
    Args:
        node_id: Node ID to analyze
        
    Returns:
        API response dictionary with analysis
    """
    url = f"{BASE_URL}/contextual-chains/nodes/{node_id}/analysis"
    response = requests.get(url)
    return response.json()


def get_chain_snapshot(node_id: str) -> Dict[str, Any]:
    """
    Get a chain snapshot starting from a node.
    
    Args:
        node_id: Root node ID
        
    Returns:
        API response dictionary with snapshot
    """
    url = f"{BASE_URL}/contextual-chains/snapshots/{node_id}"
    response = requests.get(url, params={"include_metrics": True})
    return response.json()


def create_bid_with_context(
    project_name: str,
    client_name: str,
    cost_code_ids: List[int]
) -> Dict[str, Any]:
    """
    Create a bid and contextualize it.
    
    Args:
        project_name: Project name
        client_name: Client name
        cost_code_ids: List of cost code IDs
        
    Returns:
        API response dictionary
    """
    # First create the bid
    url = f"{BASE_URL}/bids"
    line_items = []
    
    # Get cost code details
    for cc_id in cost_code_ids:
        cc_response = requests.get(f"{BASE_URL}/cost-codes/{cc_id}")
        if cc_response.status_code == 200:
            cc = cc_response.json()
            line_items.append({
                "cost_code_id": cc["id"],
                "cost_code": cc["code"],
                "description": cc["name"],
                "quantity": 1,
                "unit_price": cc["unit_price"],
                "total": cc["unit_price"]
            })
    
    bid_payload = {
        "project_name": project_name,
        "client_name": client_name,
        "line_items": line_items
    }
    
    bid_response = requests.post(url, json=bid_payload)
    bid = bid_response.json()
    
    # Contextualize the bid
    contextualize_url = f"{BASE_URL}/contextual-chains/bids/{bid['id']}/contextualize"
    context_response = requests.post(contextualize_url)
    
    return {
        "bid": bid,
        "contextual_node": context_response.json()
    }


# ============================================================================
# Example 1: Create a simple chain with cost codes and analyze
# ============================================================================
def example_1_simple_chain():
    """Example 1: Create a simple chain with cost codes and analyze heritage."""
    print("=" * 70)
    print("Example 1: Create Bid with Contextual Tracking")
    print("=" * 70)
    
    # Create cost codes
    print("\n1. Creating cost codes...")
    cc1 = create_cost_code("CC-001", "Electrical Installation", 150.0)
    cc2 = create_cost_code("CC-002", "Plumbing Work", 120.0)
    print(f"   Created: {cc1['code']} (ID: {cc1['id']})")
    print(f"   Created: {cc2['code']} (ID: {cc2['id']})")
    
    # Create bid with context
    print("\n2. Creating bid with contextual tracking...")
    result = create_bid_with_context(
        "Office Renovation",
        "Acme Corp",
        [cc1["id"], cc2["id"]]
    )
    print(f"   Bid created: {result['bid']['bid_number']}")
    print(f"   Contextual node: {result['contextual_node']['node_id']}")
    print(f"   Chain depth: {result['contextual_node']['lathering_depth']}")
    
    # Analyze the bid's heritage
    print("\n3. Analyzing bid heritage...")
    node_id = result['contextual_node']['node_id']
    analysis = analyze_node(node_id)
    print(f"   Total ancestors: {analysis['total_ancestors']}")
    print(f"   Heritage lineage: {analysis['heritage_lineage']}")
    print(f"   Chain metrics: {json.dumps(analysis['chain_metrics'], indent=2)}")
    
    print("\n✓ Example 1 completed successfully!\n")


# ============================================================================
# Example 2: Multi-level chain with snapshots
# ============================================================================
def example_2_multilevel_chain():
    """Example 2: Create a multi-level chain and generate snapshots."""
    print("=" * 70)
    print("Example 2: Multi-level Chain with Snapshots")
    print("=" * 70)
    
    # Create a hierarchical chain
    print("\n1. Creating hierarchical chain...")
    
    # Level 0: Root cost code nodes
    root1 = create_contextual_node(
        "cc-material-001",
        "cost_code",
        [],
        {"description": "Base materials"}
    )
    print(f"   Created root: {root1['node_id']} (depth: {root1['lathering_depth']})")
    
    # Level 1: Derived cost code
    derived1 = create_contextual_node(
        "cc-derived-001",
        "cost_code",
        ["cc-material-001"],
        {"description": "Derived cost code"}
    )
    print(f"   Created child: {derived1['node_id']} (depth: {derived1['lathering_depth']})")
    
    # Level 2: Bid node
    bid_node = create_contextual_node(
        "bid-example-001",
        "bid",
        ["cc-derived-001"],
        {"project": "Example Project"}
    )
    print(f"   Created bid: {bid_node['node_id']} (depth: {bid_node['lathering_depth']})")
    
    # Level 3: ROI analysis node
    roi_node = create_contextual_node(
        "roi-analysis-001",
        "roi_analysis",
        ["bid-example-001"],
        {"analysis_type": "comprehensive"}
    )
    print(f"   Created ROI: {roi_node['node_id']} (depth: {roi_node['lathering_depth']})")
    
    # Get chain snapshot
    print("\n2. Generating chain snapshot from root...")
    snapshot = get_chain_snapshot("cc-material-001")
    print(f"   Snapshot ID: {snapshot['snapshot_id']}")
    print(f"   Total nodes: {snapshot['total_nodes']}")
    print(f"   Max depth: {snapshot['max_depth']}")
    print(f"   Node tree: {json.dumps(snapshot['node_tree'], indent=2)}")
    
    print("\n✓ Example 2 completed successfully!\n")


# ============================================================================
# Example 3: Chain value flow analysis
# ============================================================================
def example_3_value_flow():
    """Example 3: Track value flow through chain."""
    print("=" * 70)
    print("Example 3: Chain Value Flow Analysis")
    print("=" * 70)
    
    print("\n1. Creating cost codes and bid...")
    
    # Create cost codes with different values
    cc1 = create_cost_code("CC-VF-001", "High Value Item", 500.0)
    cc2 = create_cost_code("CC-VF-002", "Medium Value Item", 200.0)
    cc3 = create_cost_code("CC-VF-003", "Low Value Item", 50.0)
    
    # Create bid
    result = create_bid_with_context(
        "Value Flow Demo",
        "Test Client",
        [cc1["id"], cc2["id"], cc3["id"]]
    )
    
    bid_id = result['bid']['id']
    print(f"   Bid created: {result['bid']['bid_number']}")
    print(f"   Total amount: ${result['bid']['total_amount']}")
    
    # Note: This would require adding the value flow endpoint to the API
    # For now, we demonstrate the concept
    print("\n2. Value flow would show:")
    print(f"   - Chain depth: {result['contextual_node']['lathering_depth']}")
    print(f"   - Cost codes in chain: 3")
    print(f"   - Total chain value: ${500 + 200 + 50}")
    print(f"   - Value concentration: 100%")
    
    print("\n✓ Example 3 completed successfully!\n")


# ============================================================================
# Example 4: Detect circular dependencies
# ============================================================================
def example_4_circular_detection():
    """Example 4: Demonstrate circular dependency detection."""
    print("=" * 70)
    print("Example 4: Circular Dependency Detection")
    print("=" * 70)
    
    print("\n1. Creating valid chain...")
    node_a = create_contextual_node("circ-a", "cost_code", [], {})
    node_b = create_contextual_node("circ-b", "bid", ["circ-a"], {})
    print(f"   Created: circ-a -> circ-b")
    
    print("\n2. Attempting to create circular reference...")
    try:
        # Try to create a node that references itself
        circular_node = create_contextual_node(
            "circ-self",
            "cost_code",
            ["circ-self"],  # Self-reference
            {}
        )
        print("   ✗ Circular reference was allowed (unexpected)")
    except Exception as e:
        print(f"   ✓ Circular reference prevented: {str(e)}")
    
    print("\n✓ Example 4 completed successfully!\n")


# ============================================================================
# Main execution
# ============================================================================
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("Contextual Lathering String Heritage System - Examples")
    print("=" * 70)
    print("\nMake sure the API server is running on http://localhost:8000")
    print("Start with: uvicorn app.main:app --reload")
    print("\n" + "=" * 70 + "\n")
    
    try:
        # Run examples
        example_1_simple_chain()
        example_2_multilevel_chain()
        example_3_value_flow()
        example_4_circular_detection()
        
        print("\n" + "=" * 70)
        print("All examples completed successfully!")
        print("=" * 70 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to API server")
        print("  Make sure the server is running on http://localhost:8000")
        print("  Start with: uvicorn app.main:app --reload\n")
    except Exception as e:
        print(f"\n✗ Error: {str(e)}\n")
