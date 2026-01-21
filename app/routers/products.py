from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[schemas.Product])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all products with pagination"""
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product by ID"""
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=schemas.Product, status_code=201)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """Create a new product"""
    # Check if SKU already exists
    existing = db.query(models.Product).filter(models.Product.sku == product.sku).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product with this SKU already exists")
    
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.put("/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    """Update an existing product"""
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Update only provided fields
    update_data = product.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product"""
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return None


@router.post("/quote", response_model=schemas.QuoteResponse)
def calculate_quote(quote_request: schemas.QuoteRequest, db: Session = Depends(get_db)):
    """Calculate quote with volume discounts, seasonal pricing, and tier adjustments"""
    product = db.query(models.Product).filter(models.Product.id == quote_request.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    quantity = quote_request.quantity
    base_price = product.base_price
    base_cost = product.base_cost
    
    # Calculate volume discount (5-20% based on quantity)
    volume_discount_percent = calculate_volume_discount(quantity, product.pricing_tiers)
    
    # Calculate seasonal adjustment
    seasonal_adjustment_percent = calculate_seasonal_adjustment(quote_request.season)
    
    # Calculate tier adjustment
    tier_adjustment_percent = calculate_tier_adjustment(quote_request.tier)
    
    # Calculate final unit price with all adjustments
    unit_price = base_price
    unit_price *= (1 - volume_discount_percent / 100)
    unit_price *= (1 + seasonal_adjustment_percent / 100)
    unit_price *= (1 - tier_adjustment_percent / 100)
    
    subtotal = base_price * quantity
    total_price = unit_price * quantity
    
    # Calculate margin
    total_cost = base_cost * quantity
    margin_amount = total_price - total_cost
    margin_percent = (margin_amount / total_price * 100) if total_price > 0 else 0
    
    return schemas.QuoteResponse(
        product_id=product.id,
        product_name=product.name,
        sku=product.sku,
        quantity=quantity,
        base_price=base_price,
        unit_price=round(unit_price, 2),
        volume_discount_percent=round(volume_discount_percent, 2),
        seasonal_adjustment_percent=round(seasonal_adjustment_percent, 2),
        tier_adjustment_percent=round(tier_adjustment_percent, 2),
        subtotal=round(subtotal, 2),
        total_price=round(total_price, 2),
        margin_percent=round(margin_percent, 2),
        margin_amount=round(margin_amount, 2)
    )


def calculate_volume_discount(quantity: int, pricing_tiers: dict) -> float:
    """Calculate volume discount percentage based on quantity (5-20%)"""
    # If pricing_tiers is defined in the product, use it
    if pricing_tiers:
        for tier_name, tier_data in sorted(pricing_tiers.items()):
            if quantity >= tier_data.get("min_quantity", 0):
                return tier_data.get("discount_percent", 0)
    
    # Default volume discount tiers
    if quantity >= 1000:
        return 20.0
    elif quantity >= 500:
        return 15.0
    elif quantity >= 250:
        return 12.0
    elif quantity >= 100:
        return 10.0
    elif quantity >= 50:
        return 7.0
    elif quantity >= 10:
        return 5.0
    return 0.0


def calculate_seasonal_adjustment(season: str) -> float:
    """Calculate seasonal price adjustment (positive = price increase)"""
    if not season:
        return 0.0
    
    season = season.lower()
    seasonal_adjustments = {
        "winter": 10.0,  # Higher prices in winter (demand)
        "spring": 5.0,   # Moderate increase in spring
        "summer": -5.0,  # Discount in summer (off-peak)
        "fall": 0.0      # Standard pricing in fall
    }
    return seasonal_adjustments.get(season, 0.0)


def calculate_tier_adjustment(tier: str) -> float:
    """Calculate customer tier discount (higher tier = better discount)"""
    if not tier:
        return 0.0
    
    tier = tier.lower()
    tier_discounts = {
        "standard": 0.0,    # No discount for standard customers
        "premium": 5.0,     # 5% discount for premium customers
        "enterprise": 10.0  # 10% discount for enterprise customers
    }
    return tier_discounts.get(tier, 0.0)
