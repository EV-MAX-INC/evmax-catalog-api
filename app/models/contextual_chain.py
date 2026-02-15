"""Contextual chain models for heritage tracking."""

from sqlalchemy import Column, Integer, String, JSON, DateTime, Index
from sqlalchemy.sql import func
from app.database import Base


class ContextualChainNode(Base):
    """Model for contextual chain nodes in the intermodular chain."""
    
    __tablename__ = "contextual_chain_nodes"
    
    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(String(100), unique=True, nullable=False, index=True)
    node_type = Column(String(50), nullable=False, index=True)
    parent_nodes = Column(JSON, default=list, nullable=False)
    node_metadata = Column(JSON, default=dict, nullable=False)
    lathering_depth = Column(Integer, default=0, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_node_type_depth', 'node_type', 'lathering_depth'),
    )


class HeritageLineage(Base):
    """Model for tracking heritage lineage between nodes."""
    
    __tablename__ = "heritage_lineage"
    
    id = Column(Integer, primary_key=True, index=True)
    ancestor_node_id = Column(String(100), nullable=False, index=True)
    descendant_node_id = Column(String(100), nullable=False, index=True)
    depth_distance = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('idx_ancestor_descendant', 'ancestor_node_id', 'descendant_node_id', unique=True),
        Index('idx_descendant_depth', 'descendant_node_id', 'depth_distance'),
    )
