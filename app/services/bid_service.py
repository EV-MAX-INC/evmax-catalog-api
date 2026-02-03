"""Bid service for business logic."""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.bid import Bid
from app.models.cost_code import CostCode
from app.schemas.bid import BidCreate, BidUpdate


class BidService:
    """Service class for bid operations."""

    @staticmethod
    def generate_bid_number() -> str:
        """
        Generate a unique bid number.
        
        Returns:
            Bid number in format BID-YYYYMMDD-NNNN
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"BID-{timestamp}"

    @staticmethod
    def get_bid(db: Session, bid_id: int) -> Optional[Bid]:
        """
        Get a bid by ID.
        
        Args:
            db: Database session
            bid_id: Bid ID
            
        Returns:
            Bid or None if not found
        """
        return db.query(Bid).filter(Bid.id == bid_id).first()

    @staticmethod
    def get_bid_by_number(db: Session, bid_number: str) -> Optional[Bid]:
        """
        Get a bid by its bid number.
        
        Args:
            db: Database session
            bid_number: Bid number
            
        Returns:
            Bid or None if not found
        """
        return db.query(Bid).filter(Bid.bid_number == bid_number).first()

    @staticmethod
    def get_bids(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> tuple[List[Bid], int]:
        """
        Get a list of bids with optional filtering.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            status: Filter by status
            is_active: Filter by active status
            
        Returns:
            Tuple of (bids list, total count)
        """
        query = db.query(Bid)

        if status:
            query = query.filter(Bid.status == status)

        if is_active is not None:
            query = query.filter(Bid.is_active == is_active)

        total = query.count()
        bids = query.order_by(Bid.created_at.desc()).offset(skip).limit(limit).all()

        return bids, total

    @staticmethod
    def create_bid(db: Session, bid_data: BidCreate) -> Bid:
        """
        Create a new bid with line items.
        
        Args:
            db: Database session
            bid_data: Bid data
            
        Returns:
            Created Bid
        """
        # Convert line items to dict format
        line_items_data = [item.model_dump() for item in bid_data.line_items]

        # Create bid
        db_bid = Bid(
            bid_number=BidService.generate_bid_number(),
            project_name=bid_data.project_name,
            client_name=bid_data.client_name,
            description=bid_data.description,
            tax_rate=bid_data.tax_rate,
            estimated_revenue=bid_data.estimated_revenue,
            estimated_cost=bid_data.estimated_cost,
            notes=bid_data.notes,
            valid_until=bid_data.valid_until,
            line_items=line_items_data,
        )

        # Calculate totals
        db_bid.calculate_totals()

        # Calculate ROI if revenue and cost provided
        if db_bid.estimated_revenue and db_bid.estimated_cost:
            roi_data = db_bid.calculate_roi()
            db_bid.estimated_roi_percentage = roi_data.get("roi_percentage")

        db.add(db_bid)
        db.commit()
        db.refresh(db_bid)
        return db_bid

    @staticmethod
    def update_bid(db: Session, bid_id: int, bid_data: BidUpdate) -> Optional[Bid]:
        """
        Update an existing bid.
        
        Args:
            db: Database session
            bid_id: Bid ID
            bid_data: Updated bid data
            
        Returns:
            Updated Bid or None if not found
        """
        db_bid = BidService.get_bid(db, bid_id)
        if not db_bid:
            return None

        update_data = bid_data.model_dump(exclude_unset=True)

        # Handle line items separately
        if "line_items" in update_data and update_data["line_items"]:
            update_data["line_items"] = [
                item.model_dump() if hasattr(item, "model_dump") else item
                for item in update_data["line_items"]
            ]

        for field, value in update_data.items():
            setattr(db_bid, field, value)

        # Recalculate totals if line items or tax rate changed
        if "line_items" in update_data or "tax_rate" in update_data:
            db_bid.calculate_totals()

        # Recalculate ROI if relevant fields changed
        if "estimated_revenue" in update_data or "estimated_cost" in update_data:
            if db_bid.estimated_revenue and db_bid.estimated_cost:
                roi_data = db_bid.calculate_roi()
                db_bid.estimated_roi_percentage = roi_data.get("roi_percentage")

        db.commit()
        db.refresh(db_bid)
        return db_bid

    @staticmethod
    def delete_bid(db: Session, bid_id: int) -> bool:
        """
        Delete a bid (soft delete by setting is_active to False).
        
        Args:
            db: Database session
            bid_id: Bid ID
            
        Returns:
            True if deleted, False if not found
        """
        db_bid = BidService.get_bid(db, bid_id)
        if not db_bid:
            return False

        db_bid.is_active = False
        db.commit()
        return True

    @staticmethod
    def calculate_bid_from_cost_codes(
        db: Session, line_items: List[Dict[str, Any]], tax_rate: float = 0.0
    ) -> Dict[str, Any]:
        """
        Calculate bid totals from cost codes and quantities.
        
        Args:
            db: Database session
            line_items: List of items with cost_code_id and quantity
            tax_rate: Tax rate percentage
            
        Returns:
            Dictionary with calculated bid data
        """
        calculated_items = []
        subtotal = 0.0

        for item in line_items:
            cost_code_id = item.get("cost_code_id")
            quantity = item.get("quantity", 1)

            cost_code = db.query(CostCode).filter(CostCode.id == cost_code_id).first()
            if not cost_code:
                continue

            line_total = cost_code.calculate_total_cost(quantity)
            subtotal += line_total

            calculated_items.append({
                "cost_code_id": cost_code.id,
                "cost_code": cost_code.code,
                "description": cost_code.name,
                "quantity": quantity,
                "unit": cost_code.unit,
                "unit_price": cost_code.unit_price,
                "total": round(line_total, 2),
            })

        tax_amount = subtotal * (tax_rate / 100)
        total_amount = subtotal + tax_amount

        return {
            "line_items": calculated_items,
            "subtotal": round(subtotal, 2),
            "tax_amount": round(tax_amount, 2),
            "total_amount": round(total_amount, 2),
        }

    @staticmethod
    def calculate_roi_analysis(
        estimated_revenue: float,
        estimated_cost: float,
        project_duration_months: int,
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive ROI analysis.
        
        Args:
            estimated_revenue: Estimated project revenue
            estimated_cost: Estimated project cost
            project_duration_months: Project duration in months
            
        Returns:
            Dictionary with ROI analysis
        """
        profit = estimated_revenue - estimated_cost
        roi_percentage = (profit / estimated_cost) * 100 if estimated_cost > 0 else 0
        
        # Calculate payback period in months
        monthly_profit = profit / project_duration_months if project_duration_months > 0 else 0
        payback_months = (
            int(estimated_cost / monthly_profit) if monthly_profit > 0 else 0
        )

        return {
            "roi_percentage": round(roi_percentage, 2),
            "profit": round(profit, 2),
            "payback_months": payback_months,
            "estimated_revenue": estimated_revenue,
            "estimated_cost": estimated_cost,
            "monthly_profit": round(monthly_profit, 2) if monthly_profit > 0 else 0,
        }
