"""Cost code service for business logic."""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.cost_code import CostCode
from app.schemas.cost_code import CostCodeCreate, CostCodeUpdate


class CostCodeService:
    """Service class for cost code operations."""

    @staticmethod
    def get_cost_code(db: Session, cost_code_id: int) -> Optional[CostCode]:
        """
        Get a cost code by ID.
        
        Args:
            db: Database session
            cost_code_id: Cost code ID
            
        Returns:
            CostCode or None if not found
        """
        return db.query(CostCode).filter(CostCode.id == cost_code_id).first()

    @staticmethod
    def get_cost_code_by_code(db: Session, code: str) -> Optional[CostCode]:
        """
        Get a cost code by its code string.
        
        Args:
            db: Database session
            code: Cost code string
            
        Returns:
            CostCode or None if not found
        """
        return db.query(CostCode).filter(CostCode.code == code.upper()).first()

    @staticmethod
    def get_cost_codes(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        is_active: Optional[bool] = None,
        search: Optional[str] = None,
    ) -> tuple[List[CostCode], int]:
        """
        Get a list of cost codes with optional filtering.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            category: Filter by category
            is_active: Filter by active status
            search: Search term for code, name, or description
            
        Returns:
            Tuple of (cost codes list, total count)
        """
        query = db.query(CostCode)

        if category:
            query = query.filter(CostCode.category == category)

        if is_active is not None:
            query = query.filter(CostCode.is_active == is_active)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    CostCode.code.ilike(search_term),
                    CostCode.name.ilike(search_term),
                    CostCode.description.ilike(search_term),
                )
            )

        total = query.count()
        cost_codes = query.offset(skip).limit(limit).all()

        return cost_codes, total

    @staticmethod
    def create_cost_code(db: Session, cost_code_data: CostCodeCreate) -> CostCode:
        """
        Create a new cost code.
        
        Args:
            db: Database session
            cost_code_data: Cost code data
            
        Returns:
            Created CostCode
        """
        db_cost_code = CostCode(**cost_code_data.model_dump())
        db.add(db_cost_code)
        db.commit()
        db.refresh(db_cost_code)
        return db_cost_code

    @staticmethod
    def update_cost_code(
        db: Session, cost_code_id: int, cost_code_data: CostCodeUpdate
    ) -> Optional[CostCode]:
        """
        Update an existing cost code.
        
        Args:
            db: Database session
            cost_code_id: Cost code ID
            cost_code_data: Updated cost code data
            
        Returns:
            Updated CostCode or None if not found
        """
        db_cost_code = CostCodeService.get_cost_code(db, cost_code_id)
        if not db_cost_code:
            return None

        update_data = cost_code_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_cost_code, field, value)

        db.commit()
        db.refresh(db_cost_code)
        return db_cost_code

    @staticmethod
    def delete_cost_code(db: Session, cost_code_id: int) -> bool:
        """
        Delete a cost code (soft delete by setting is_active to False).
        
        Args:
            db: Database session
            cost_code_id: Cost code ID
            
        Returns:
            True if deleted, False if not found
        """
        db_cost_code = CostCodeService.get_cost_code(db, cost_code_id)
        if not db_cost_code:
            return False

        db_cost_code.is_active = False
        db.commit()
        return True
