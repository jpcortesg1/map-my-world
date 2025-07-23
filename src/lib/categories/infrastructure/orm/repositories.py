"""SQLAlchemy repository implementation for categories."""
from typing import List, Optional
from sqlalchemy.orm import Session
from ...domain.entities import Category
from ...domain.repositories import CategoryRepository
from .models import CategoryModel
from src.shared.logging.logger import get_logger

logger = get_logger(__name__)


class CategoryRepositoryImpl(CategoryRepository):
    """SQLAlchemy implementation of CategoryRepository."""
    
    def __init__(self, session: Session) -> None:
        self.session = session
    
    async def create(self, category: Category) -> Category:
        """Create a new category."""
        logger.info(f"Creating category in database: {category.name}")
        
        try:
            category_model = CategoryModel.from_domain(category)
            self.session.add(category_model)
            self.session.commit()
            self.session.refresh(category_model)
            
            logger.info(f"Category created in database: {category_model.id}")
            return category_model.to_domain()
        except Exception as e:
            logger.error(f"Error creating category: {e}")
            self.session.rollback()
            raise
    
    async def get_by_id(self, category_id: int) -> Optional[Category]:
        """Get category by ID."""
        logger.info(f"Getting category from database: {category_id}")
        
        category_model = self.session.query(CategoryModel).filter(CategoryModel.id == category_id).first()
        
        if category_model:
            logger.info(f"Category found in database: {category_id}")
            return category_model.to_domain()
        
        logger.warning(f"Category not found in database: {category_id}")
        return None
    
    async def get_all(
        self, 
        limit: Optional[int] = None,
        offset: int = 0,
        name_filter: Optional[str] = None
    ) -> List[Category]:
        """Get all categories with optional filtering and pagination."""
        logger.info(f"Getting categories from database: limit={limit}, offset={offset}, name_filter={name_filter}")
        
        query = self.session.query(CategoryModel)
        
        # Apply name filter if provided
        if name_filter:
            query = query.filter(CategoryModel.name.ilike(f"%{name_filter}%"))
        
        # Apply ordering for consistent pagination
        query = query.order_by(CategoryModel.id)
        
        # Apply offset
        if offset > 0:
            query = query.offset(offset)
        
        # Apply limit
        if limit:
            query = query.limit(limit)
        
        category_models = query.all()
        categories = [model.to_domain() for model in category_models]
        
        logger.info(f"Retrieved {len(categories)} categories from database")
        return categories
    
    async def update(self, category: Category) -> Optional[Category]:
        """Update an existing category."""
        logger.info(f"Updating category in database: {category.id}")
        
        try:
            category_model = self.session.query(CategoryModel).filter(CategoryModel.id == category.id).first()
            
            if not category_model:
                logger.warning(f"Category not found for update: {category.id}")
                return None
            
            # Update fields
            category_model.name = category.name
            if category.description is not None:
                category_model.description = category.description
            category_model.updated_at = category.updated_at
            
            self.session.commit()
            self.session.refresh(category_model)
            
            logger.info(f"Category updated in database: {category.id}")
            return category_model.to_domain()
        except Exception as e:
            logger.error(f"Error updating category: {e}")
            self.session.rollback()
            raise
    
    async def delete(self, category_id: int) -> bool:
        """Delete a category by ID."""
        logger.info(f"Deleting category from database: {category_id}")
        
        try:
            category_model = self.session.query(CategoryModel).filter(CategoryModel.id == category_id).first()
            
            if not category_model:
                logger.warning(f"Category not found for deletion: {category_id}")
                return False
            
            self.session.delete(category_model)
            self.session.commit()
            
            logger.info(f"Category deleted from database: {category_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting category: {e}")
            self.session.rollback()
            raise
    
    async def exists_by_name(self, name: str) -> bool:
        """Check if category exists by name."""
        logger.info(f"Checking if category exists: {name}")
        
        exists = self.session.query(CategoryModel).filter(CategoryModel.name == name).first() is not None
        
        logger.info(f"Category exists check result: {exists}")
        return exists 