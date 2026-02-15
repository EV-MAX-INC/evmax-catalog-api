"""Pydantic schemas for contextual chain."""

from pydantic import BaseModel, Field, field_serializer
from typing import List, Dict, Any, Optional
from datetime import datetime


class ContextualChainNodeCreate(BaseModel):
    """Schema for creating a contextual chain node."""
    
    node_id: str = Field(..., min_length=1, max_length=100)
    node_type: str = Field(..., min_length=1, max_length=50)
    parent_nodes: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ContextualChainNodeResponse(BaseModel):
    """Schema for contextual chain node response."""
    
    id: int
    node_id: str
    node_type: str
    parent_nodes: List[str]
    metadata: Dict[str, Any] = Field(alias="node_metadata")
    lathering_depth: int
    created_at: datetime
    
    model_config = {"from_attributes": True, "populate_by_name": True}


class ChainAnalysisResponse(BaseModel):
    """Schema for chain analysis response."""
    
    node_id: str
    lathering_depth: int
    heritage_lineage: List[str]
    total_ancestors: int
    chain_metrics: Dict[str, Any]
    value_flow: Optional[float] = None


class ChainSnapshotResponse(BaseModel):
    """Schema for chain snapshot response."""
    
    snapshot_id: str
    root_node: str
    total_nodes: int
    max_depth: int
    node_tree: Dict[str, Any]
    generated_at: datetime
