"""SQLAlchemy models for categories."""
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from config.database import Base
from ...domain.entities import Category


class CategoryModel(Base):
    """SQLAlchemy model for categories table."""
    
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def to_domain(self) -> Category:
        """Convert model to domain entity."""
        return Category(
            id=self.id,
            name=self.name,
            description=self.description,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain(cls, category: Category) -> "CategoryModel":
        """Create model from domain entity."""
        model = cls(
            name=category.name,
            description=category.description,
            created_at=category.created_at,
            updated_at=category.updated_at
        )
        # Only set id if it's not None (for updates)
        if category.id is not None:
            model.id = category.id
        return model 