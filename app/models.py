from sqlalchemy import Column, Integer, String, Float, Text, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(100), unique=True, index=True, nullable=False)
    category = Column(String(100), index=True)
    name = Column(String(255), nullable=False)
    base_cost = Column(Float, nullable=False)
    base_price = Column(Float, nullable=False)
    pricing_tiers = Column(JSON)  # JSONB for PostgreSQL - stores volume discount tiers
    material_specs = Column(JSON)  # JSONB for material specifications
    compliance_codes = Column(String(500))  # Comma-separated compliance codes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class CostCode(Base):
    __tablename__ = "cost_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(Text)
    category = Column(String(100))
    base_rate = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ComplianceStandard(Base):
    __tablename__ = "compliance_standards"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    issuing_body = Column(String(255))
    effective_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
