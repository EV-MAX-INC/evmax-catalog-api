"""Contextual lathering service for heritage tracking and chain analysis."""

import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.models.contextual_chain import ContextualChainNode, HeritageLineage
from app.config import settings

logger = logging.getLogger(__name__)


@dataclass
class ContextualChainNodeData:
    """Data structure representing a node in the intermodular chain."""
    
    node_id: str
    node_type: str
    parent_nodes: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    lathering_depth: int = 0


class ContextualLatheringEngine:
    """Engine for managing contextual chain nodes and heritage tracking."""
    
    def __init__(self, db: Session):
        """
        Initialize the contextual lathering engine.
        
        Args:
            db: Database session
        """
        self.db = db
    
    def register_node(self, node: ContextualChainNodeData) -> str:
        """
        Register a new node in the contextual chain.
        
        Args:
            node: Contextual chain node data
            
        Returns:
            Node ID of the registered node
            
        Raises:
            ValueError: If node already exists or circular dependency detected
        """
        # Check if node already exists
        existing = self.db.query(ContextualChainNode).filter(
            ContextualChainNode.node_id == node.node_id
        ).first()
        
        if existing:
            raise ValueError(f"Node with ID {node.node_id} already exists")
        
        # Check for circular dependencies if enabled
        if settings.ENABLE_CIRCULAR_DEPENDENCY_CHECK:
            if self._would_create_cycle(node.node_id, node.parent_nodes):
                raise ValueError(
                    f"Cannot register node {node.node_id}: would create circular dependency"
                )
        
        # Calculate lathering depth
        depth = self._calculate_depth(node.parent_nodes)
        
        # Validate against max depth
        if depth > settings.MAX_CHAIN_DEPTH:
            raise ValueError(
                f"Cannot register node: depth {depth} exceeds maximum {settings.MAX_CHAIN_DEPTH}"
            )
        
        # Create the node
        db_node = ContextualChainNode(
            node_id=node.node_id,
            node_type=node.node_type,
            parent_nodes=node.parent_nodes,
            node_metadata=node.metadata,
            lathering_depth=depth,
        )
        
        self.db.add(db_node)
        self.db.flush()
        
        # Create heritage lineage entries
        self._create_heritage_entries(node.node_id, node.parent_nodes, depth)
        
        self.db.commit()
        logger.info(f"Registered node {node.node_id} with depth {depth}")
        
        return node.node_id
    
    def calculate_lathering_depth(self, node_id: str) -> int:
        """
        Calculate the lathering depth for a node.
        
        Args:
            node_id: Node ID
            
        Returns:
            Lathering depth (0 for root nodes)
            
        Raises:
            ValueError: If node not found
        """
        node = self.db.query(ContextualChainNode).filter(
            ContextualChainNode.node_id == node_id
        ).first()
        
        if not node:
            raise ValueError(f"Node {node_id} not found")
        
        return node.lathering_depth
    
    def get_heritage_lineage(self, node_id: str) -> List[str]:
        """
        Get the complete heritage lineage for a node.
        
        Args:
            node_id: Node ID
            
        Returns:
            List of ancestor node IDs ordered by depth (closest to furthest)
            
        Raises:
            ValueError: If node not found
        """
        node = self.db.query(ContextualChainNode).filter(
            ContextualChainNode.node_id == node_id
        ).first()
        
        if not node:
            raise ValueError(f"Node {node_id} not found")
        
        # Query all ancestors ordered by depth
        lineage = self.db.query(HeritageLineage).filter(
            HeritageLineage.descendant_node_id == node_id
        ).order_by(HeritageLineage.depth_distance).all()
        
        return [entry.ancestor_node_id for entry in lineage]
    
    def analyze_chain_metrics(self, node_id: str) -> Dict[str, Any]:
        """
        Analyze comprehensive metrics for a node's chain.
        
        Args:
            node_id: Node ID
            
        Returns:
            Dictionary containing chain metrics
            
        Raises:
            ValueError: If node not found
        """
        node = self.db.query(ContextualChainNode).filter(
            ContextualChainNode.node_id == node_id
        ).first()
        
        if not node:
            raise ValueError(f"Node {node_id} not found")
        
        # Get heritage lineage
        lineage = self.get_heritage_lineage(node_id)
        
        # Count descendants
        descendants_count = self.db.query(HeritageLineage).filter(
            HeritageLineage.ancestor_node_id == node_id
        ).count()
        
        # Get node type distribution in lineage
        if lineage:
            ancestor_nodes = self.db.query(ContextualChainNode).filter(
                ContextualChainNode.node_id.in_(lineage)
            ).all()
            node_type_distribution = {}
            for ancestor in ancestor_nodes:
                node_type_distribution[ancestor.node_type] = \
                    node_type_distribution.get(ancestor.node_type, 0) + 1
        else:
            node_type_distribution = {}
        
        return {
            "node_id": node_id,
            "node_type": node.node_type,
            "lathering_depth": node.lathering_depth,
            "total_ancestors": len(lineage),
            "total_descendants": descendants_count,
            "node_type_distribution": node_type_distribution,
            "parent_nodes": node.parent_nodes,
            "is_root": len(node.parent_nodes) == 0,
            "is_leaf": descendants_count == 0,
            "created_at": node.created_at.isoformat() if node.created_at else None,
        }
    
    def detect_circular_dependencies(self, node_id: str) -> bool:
        """
        Detect if adding this node would create a circular dependency.
        
        Args:
            node_id: Node ID to check
            
        Returns:
            True if circular dependency detected, False otherwise
        """
        node = self.db.query(ContextualChainNode).filter(
            ContextualChainNode.node_id == node_id
        ).first()
        
        if not node:
            return False
        
        return self._would_create_cycle(node_id, node.parent_nodes)
    
    def get_chain_snapshot(
        self,
        root_node_id: str,
        include_metrics: bool = True
    ) -> Dict[str, Any]:
        """
        Generate a snapshot of the entire chain starting from a root node.
        
        Args:
            root_node_id: Root node ID to start snapshot from
            include_metrics: Whether to include detailed metrics
            
        Returns:
            Dictionary containing chain snapshot data
            
        Raises:
            ValueError: If node not found
        """
        root_node = self.db.query(ContextualChainNode).filter(
            ContextualChainNode.node_id == root_node_id
        ).first()
        
        if not root_node:
            raise ValueError(f"Root node {root_node_id} not found")
        
        # Build the tree structure
        node_tree = self._build_node_tree(root_node_id)
        
        # Calculate total nodes and max depth
        all_descendants = self.db.query(HeritageLineage).filter(
            HeritageLineage.ancestor_node_id == root_node_id
        ).all()
        
        max_depth = root_node.lathering_depth
        if all_descendants:
            descendant_ids = [d.descendant_node_id for d in all_descendants]
            descendant_nodes = self.db.query(ContextualChainNode).filter(
                ContextualChainNode.node_id.in_(descendant_ids)
            ).all()
            if descendant_nodes:
                max_depth = max(n.lathering_depth for n in descendant_nodes)
        
        snapshot = {
            "snapshot_id": f"SNAP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "root_node": root_node_id,
            "total_nodes": len(all_descendants) + 1,  # +1 for root
            "max_depth": max_depth,
            "node_tree": node_tree,
            "generated_at": datetime.now(),
        }
        
        if include_metrics:
            snapshot["metrics"] = self.analyze_chain_metrics(root_node_id)
        
        return snapshot
    
    def _calculate_depth(self, parent_nodes: List[str]) -> int:
        """
        Calculate depth based on parent nodes.
        
        Args:
            parent_nodes: List of parent node IDs
            
        Returns:
            Calculated depth
        """
        if not parent_nodes:
            return 0
        
        # Get max depth from all parents and add 1
        parent_depths = self.db.query(ContextualChainNode.lathering_depth).filter(
            ContextualChainNode.node_id.in_(parent_nodes)
        ).all()
        
        if not parent_depths:
            return 1
        
        max_parent_depth = max(depth[0] for depth in parent_depths)
        return max_parent_depth + 1
    
    def _create_heritage_entries(
        self,
        node_id: str,
        parent_nodes: List[str],
        node_depth: int
    ):
        """
        Create heritage lineage entries for a new node.
        
        Args:
            node_id: New node ID
            parent_nodes: List of parent node IDs
            node_depth: Depth of the new node
        """
        # Direct parent relationships
        for parent_id in parent_nodes:
            lineage = HeritageLineage(
                ancestor_node_id=parent_id,
                descendant_node_id=node_id,
                depth_distance=1
            )
            self.db.add(lineage)
        
        # Inherit all ancestor relationships
        for parent_id in parent_nodes:
            parent_ancestors = self.db.query(HeritageLineage).filter(
                HeritageLineage.descendant_node_id == parent_id
            ).all()
            
            for ancestor in parent_ancestors:
                lineage = HeritageLineage(
                    ancestor_node_id=ancestor.ancestor_node_id,
                    descendant_node_id=node_id,
                    depth_distance=ancestor.depth_distance + 1
                )
                self.db.add(lineage)
    
    def _would_create_cycle(self, node_id: str, parent_nodes: List[str]) -> bool:
        """
        Check if adding parents to a node would create a cycle.
        
        Args:
            node_id: Node ID
            parent_nodes: Proposed parent node IDs
            
        Returns:
            True if cycle would be created
        """
        # If node_id is in parent_nodes, direct cycle
        if node_id in parent_nodes:
            return True
        
        # Check if any parent is a descendant of this node
        for parent_id in parent_nodes:
            descendants = self.db.query(HeritageLineage).filter(
                HeritageLineage.ancestor_node_id == node_id,
                HeritageLineage.descendant_node_id == parent_id
            ).first()
            
            if descendants:
                return True
        
        return False
    
    def _build_node_tree(self, node_id: str, visited: Optional[Set[str]] = None) -> Dict[str, Any]:
        """
        Build a tree structure for visualization.
        
        Args:
            node_id: Starting node ID
            visited: Set of visited nodes to prevent cycles
            
        Returns:
            Tree structure as nested dictionary
        """
        if visited is None:
            visited = set()
        
        if node_id in visited:
            return {"node_id": node_id, "cycle_detected": True}
        
        visited.add(node_id)
        
        node = self.db.query(ContextualChainNode).filter(
            ContextualChainNode.node_id == node_id
        ).first()
        
        if not node:
            return {"node_id": node_id, "error": "not_found"}
        
        # Find direct children
        children_lineage = self.db.query(HeritageLineage).filter(
            HeritageLineage.ancestor_node_id == node_id,
            HeritageLineage.depth_distance == 1
        ).all()
        
        children = []
        for child_lineage in children_lineage:
            child_tree = self._build_node_tree(child_lineage.descendant_node_id, visited.copy())
            children.append(child_tree)
        
        return {
            "node_id": node_id,
            "node_type": node.node_type,
            "depth": node.lathering_depth,
            "children": children,
            "metadata": node.node_metadata,
        }


class ContextualLatheringService:
    """High-level service for contextual chain operations."""
    
    @staticmethod
    def create_node(
        db: Session,
        node_id: str,
        node_type: str,
        parent_nodes: List[str] = None,
        metadata: Dict[str, Any] = None
    ) -> ContextualChainNode:
        """
        Create a new contextual chain node.
        
        Args:
            db: Database session
            node_id: Unique node identifier
            node_type: Type of node
            parent_nodes: List of parent node IDs
            metadata: Additional metadata
            
        Returns:
            Created ContextualChainNode
        """
        engine = ContextualLatheringEngine(db)
        
        node_data = ContextualChainNodeData(
            node_id=node_id,
            node_type=node_type,
            parent_nodes=parent_nodes or [],
            metadata=metadata or {}
        )
        
        engine.register_node(node_data)
        
        return db.query(ContextualChainNode).filter(
            ContextualChainNode.node_id == node_id
        ).first()
    
    @staticmethod
    def get_node_analysis(db: Session, node_id: str) -> Dict[str, Any]:
        """
        Get comprehensive analysis for a node.
        
        Args:
            db: Database session
            node_id: Node ID to analyze
            
        Returns:
            Analysis dictionary
        """
        engine = ContextualLatheringEngine(db)
        
        metrics = engine.analyze_chain_metrics(node_id)
        lineage = engine.get_heritage_lineage(node_id)
        
        return {
            "node_id": node_id,
            "lathering_depth": metrics["lathering_depth"],
            "heritage_lineage": lineage,
            "total_ancestors": len(lineage),
            "chain_metrics": metrics,
            "value_flow": None  # To be implemented with bid integration
        }
    
    @staticmethod
    def get_chain_snapshot(
        db: Session,
        node_id: str,
        include_metrics: bool = True
    ) -> Dict[str, Any]:
        """
        Get complete chain snapshot.
        
        Args:
            db: Database session
            node_id: Root node ID
            include_metrics: Whether to include metrics
            
        Returns:
            Chain snapshot dictionary
        """
        engine = ContextualLatheringEngine(db)
        return engine.get_chain_snapshot(node_id, include_metrics)
