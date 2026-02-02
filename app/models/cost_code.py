"""Cost code database model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean
from sqlalchemy.sql import func

from app.database import Base


class CostCode(Base):
    """
    Cost Code model for construction cost catalog.
    
    Represents individual cost items in the construction catalog
    with pricing, descriptions, and metadata.
    """

    __tablename__ = "cost_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), index=True, nullable=False)
    unit = Column(String(50), nullable=False)  # e.g., 'EA', 'LF', 'SQ FT'
    unit_price = Column(Float, nullable=False)
    labor_cost = Column(Float, default=0.0)
    material_cost = Column(Float, default=0.0)
    equipment_cost = Column(Float, default=0.0)
    markup_percentage = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True, index=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    def __repr__(self) -> str:
        """String representation of CostCode."""
        return f"<CostCode(code='{self.code}', name='{self.name}', unit_price={self.unit_price})>"

    def calculate_total_cost(self, quantity: float) -> float:
        """
        Calculate total cost for a given quantity.
        
        Args:
            quantity: Quantity to calculate cost for
            
        Returns:
            Total cost including markup
        """
        base_cost = self.unit_price * quantity
        markup_amount = base_cost * (self.markup_percentage / 100)
        return base_cost + markup_amount
