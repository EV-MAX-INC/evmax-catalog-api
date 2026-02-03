"""Bid database model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, JSON
from sqlalchemy.sql import func

from app.database import Base


class Bid(Base):
    """
    Bid model for automated bid calculations.
    
    Represents a bid for a project with line items and calculations.
    """

    __tablename__ = "bids"

    id = Column(Integer, primary_key=True, index=True)
    bid_number = Column(String(50), unique=True, index=True, nullable=False)
    project_name = Column(String(255), nullable=False)
    client_name = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="draft", index=True)  # draft, submitted, accepted, rejected
    
    # Cost breakdown
    subtotal = Column(Float, default=0.0)
    tax_rate = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    total_amount = Column(Float, default=0.0)
    
    # ROI Analysis fields
    estimated_revenue = Column(Float, nullable=True)
    estimated_cost = Column(Float, nullable=True)
    estimated_roi_percentage = Column(Float, nullable=True)
    estimated_payback_months = Column(Integer, nullable=True)
    
    # Line items stored as JSON
    line_items = Column(JSON, default=list)
    
    # Metadata
    notes = Column(Text, nullable=True)
    valid_until = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    def __repr__(self) -> str:
        """String representation of Bid."""
        return f"<Bid(bid_number='{self.bid_number}', project='{self.project_name}', total={self.total_amount})>"

    def calculate_totals(self) -> None:
        """Calculate bid totals from line items."""
        self.subtotal = sum(item.get("total", 0) for item in self.line_items or [])
        self.tax_amount = self.subtotal * (self.tax_rate / 100)
        self.total_amount = self.subtotal + self.tax_amount

    def calculate_roi(self) -> dict:
        """
        Calculate ROI metrics.
        
        Returns:
            Dictionary with ROI calculations
        """
        if not self.estimated_revenue or not self.estimated_cost:
            return {}
        
        roi = ((self.estimated_revenue - self.estimated_cost) / self.estimated_cost) * 100
        profit = self.estimated_revenue - self.estimated_cost
        
        return {
            "roi_percentage": round(roi, 2),
            "profit": round(profit, 2),
            "estimated_revenue": self.estimated_revenue,
            "estimated_cost": self.estimated_cost,
        }
