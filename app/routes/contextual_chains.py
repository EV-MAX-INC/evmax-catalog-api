"""API routes for contextual chain management."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.services.contextual_service import ContextualLatheringService
from app.schemas.contextual_chain import (
    ContextualChainNodeCreate,
    ContextualChainNodeResponse,
    ChainAnalysisResponse,
    ChainSnapshotResponse,
)

router = APIRouter(prefix="/contextual-chains", tags=["Contextual Chains"])


@router.post("/nodes", response_model=ContextualChainNodeResponse, status_code=201)
def create_chain_node(
    node_data: ContextualChainNodeCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new contextual chain node.
    
    Args:
        node_data: Node creation data
        db: Database session
        
    Returns:
        Created node data
        
    Raises:
        HTTPException: If node creation fails
    """
    try:
        node = ContextualLatheringService.create_node(
            db=db,
            node_id=node_data.node_id,
            node_type=node_data.node_type,
            parent_nodes=node_data.parent_nodes,
            metadata=node_data.metadata
        )
        return node
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create node: {str(e)}")


@router.get("/nodes/{node_id}/analysis", response_model=ChainAnalysisResponse)
def analyze_chain_node(
    node_id: str,
    db: Session = Depends(get_db)
):
    """
    Analyze complete heritage and metrics for a node.
    
    Args:
        node_id: Node ID to analyze
        db: Database session
        
    Returns:
        Node analysis data
        
    Raises:
        HTTPException: If node not found or analysis fails
    """
    try:
        analysis = ContextualLatheringService.get_node_analysis(db, node_id)
        return analysis
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze node: {str(e)}")


@router.get("/bids/{bid_id}/heritage", response_model=ChainAnalysisResponse)
def get_bid_heritage(
    bid_id: int,
    db: Session = Depends(get_db)
):
    """
    Get complete heritage analysis for a bid.
    
    Args:
        bid_id: Bid ID
        db: Database session
        
    Returns:
        Bid heritage analysis
        
    Raises:
        HTTPException: If bid not found or analysis fails
    """
    try:
        # Generate node ID from bid ID
        node_id = f"bid-{bid_id}"
        analysis = ContextualLatheringService.get_node_analysis(db, node_id)
        return analysis
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get bid heritage: {str(e)}")


@router.get("/snapshots/{node_id}", response_model=ChainSnapshotResponse)
def get_chain_snapshot(
    node_id: str,
    include_metrics: bool = Query(True, description="Include detailed metrics in snapshot"),
    db: Session = Depends(get_db)
):
    """
    Get complete chain snapshot with metrics.
    
    Args:
        node_id: Root node ID for snapshot
        include_metrics: Whether to include detailed metrics
        db: Database session
        
    Returns:
        Chain snapshot data
        
    Raises:
        HTTPException: If node not found or snapshot generation fails
    """
    try:
        snapshot = ContextualLatheringService.get_chain_snapshot(
            db=db,
            node_id=node_id,
            include_metrics=include_metrics
        )
        return snapshot
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate snapshot: {str(e)}")


@router.post("/bids/{bid_id}/contextualize", response_model=ContextualChainNodeResponse, status_code=201)
def contextualize_bid(
    bid_id: int,
    db: Session = Depends(get_db)
):
    """
    Create contextual chain entry for existing bid.
    
    Args:
        bid_id: Bid ID to contextualize
        db: Database session
        
    Returns:
        Created contextual node
        
    Raises:
        HTTPException: If bid not found or contextualization fails
    """
    from app.services.bid_service import BidService
    
    try:
        # Get the bid
        bid = BidService.get_bid(db, bid_id)
        if not bid:
            raise HTTPException(status_code=404, detail=f"Bid {bid_id} not found")
        
        # Extract parent nodes from bid line items (cost codes)
        parent_nodes = []
        if bid.line_items:
            for item in bid.line_items:
                if isinstance(item, dict) and "cost_code_id" in item:
                    parent_nodes.append(f"cost-code-{item['cost_code_id']}")
        
        # Create contextual node
        node_id = f"bid-{bid_id}"
        node = ContextualLatheringService.create_node(
            db=db,
            node_id=node_id,
            node_type="bid",
            parent_nodes=parent_nodes,
            metadata={
                "bid_number": bid.bid_number,
                "project_name": bid.project_name,
                "client_name": bid.client_name,
                "status": bid.status,
                "total_amount": str(bid.total_amount) if bid.total_amount else None,
            }
        )
        return node
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to contextualize bid: {str(e)}")
