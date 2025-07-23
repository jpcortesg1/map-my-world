"""SQLAlchemy models for recommendations."""
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from config.database import Base
from ...domain.entities import LocationCategoryReview


class LocationCategoryReviewModel(Base):
    """SQLAlchemy model for location_category_reviewed table."""
    
    __tablename__ = "location_category_reviewed"
    
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False, index=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Optimized indexes for recommendation queries
    __table_args__ = (
        Index('idx_location_category_reviewed_date', 'reviewed_at'),
        Index('idx_location_category_reviewed_composite', 'location_id', 'category_id', 'reviewed_at'),
    )
    
    def to_domain(self) -> LocationCategoryReview:
        """Convert model to domain entity."""
        return LocationCategoryReview(
            id=self.id,
            location_id=self.location_id,
            category_id=self.category_id,
            reviewed_at=self.reviewed_at,
            created_at=self.created_at
        )
    
    @classmethod
    def from_domain(cls, review: LocationCategoryReview) -> "LocationCategoryReviewModel":
        """Create model from domain entity."""
        return cls(
            id=review.id,
            location_id=review.location_id,
            category_id=review.category_id,
            reviewed_at=review.reviewed_at,
            created_at=review.created_at
        ) 