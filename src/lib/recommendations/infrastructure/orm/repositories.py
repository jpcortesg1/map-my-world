"""SQLAlchemy repository implementation for recommendations."""
from typing import List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import text
from ...domain.entities import LocationCategoryReview
from ...domain.repositories import RecommendationRepository
from .models import LocationCategoryReviewModel
from src.lib.locations.infrastructure.orm.models import LocationModel
from src.lib.categories.infrastructure.orm.models import CategoryModel
from src.shared.logging.logger import get_logger

logger = get_logger(__name__)


class RecommendationRepositoryImpl(RecommendationRepository):
    """SQLAlchemy implementation of RecommendationRepository."""
    
    def __init__(self, session: Session) -> None:
        self.session = session
    
    async def get_unreviewed_combinations(self, limit: int = 10) -> List[dict]:
        """Get location-category combinations not reviewed in the last 30 days."""
        logger.info(f"Getting unreviewed combinations with limit: {limit}")
        
        # Optimized SQL query for recommendations
        query = text("""
            SELECT 
                l.id as location_id,
                l.name as location_name,
                l.longitude,
                l.latitude,
                c.id as category_id,
                c.name as category_name,
                lcr.reviewed_at
            FROM locations l
            CROSS JOIN categories c
            LEFT JOIN location_category_reviewed lcr 
                ON l.id = lcr.location_id AND c.id = lcr.category_id
            WHERE lcr.reviewed_at IS NULL 
                OR lcr.reviewed_at < datetime('now', '-30 days')
            ORDER BY 
                lcr.reviewed_at IS NULL DESC,  -- Never reviewed first
                lcr.reviewed_at ASC            -- Then oldest ones
            LIMIT :limit
        """)
        
        result = self.session.execute(query, {"limit": limit})
        
        # Convert to dictionary format for API response
        combinations = []
        for row in result:
            combination = {
                "location_id": row.location_id,
                "location_name": row.location_name,
                "longitude": row.longitude,
                "latitude": row.latitude,
                "category_id": row.category_id,
                "category_name": row.category_name,
                "reviewed_at": row.reviewed_at,
            }
            combinations.append(combination)
        
        logger.info(f"Retrieved {len(combinations)} unreviewed combinations")
        return combinations
    
    async def mark_as_reviewed(self, location_id: int, category_id: int) -> LocationCategoryReview:
        """Mark a location-category combination as reviewed."""
        logger.info(f"Marking location {location_id} - category {category_id} as reviewed")
        
        try:
            # Check if record exists
            existing_review = self.session.query(LocationCategoryReviewModel).filter(
                LocationCategoryReviewModel.location_id == location_id,
                LocationCategoryReviewModel.category_id == category_id
            ).first()
            
            now = datetime.utcnow()
            
            if existing_review:
                # Update existing record
                existing_review.reviewed_at = now
                self.session.commit()
                self.session.refresh(existing_review)
                
                logger.info(f"Updated existing review record: {existing_review.id}")
                return existing_review.to_domain()
            else:
                # Create new record
                new_review = LocationCategoryReviewModel(
                    location_id=location_id,
                    category_id=category_id,
                    reviewed_at=now,
                    created_at=now
                )
                
                self.session.add(new_review)
                self.session.commit()
                self.session.refresh(new_review)
                
                logger.info(f"Created new review record: {new_review.id}")
                return new_review.to_domain()
        except Exception as e:
            logger.error(f"Error marking as reviewed: {e}")
            self.session.rollback()
            raise
    
    async def get_reviewed_combinations(self, location_id: int, category_id: int) -> List[LocationCategoryReview]:
        """Get reviewed combinations for a specific location and category."""
        logger.info(f"Getting reviewed combinations for location {location_id} - category {category_id}")
        
        reviews = self.session.query(LocationCategoryReviewModel).filter(
            LocationCategoryReviewModel.location_id == location_id,
            LocationCategoryReviewModel.category_id == category_id,
            LocationCategoryReviewModel.reviewed_at.isnot(None)
        ).all()
        
        domain_reviews = [review.to_domain() for review in reviews]
        
        logger.info(f"Retrieved {len(domain_reviews)} reviewed combinations")
        return domain_reviews
    
    async def check_location_exists(self, location_id: int) -> bool:
        """Check if a location exists by ID."""
        logger.info(f"Checking if location {location_id} exists")
        
        location = self.session.query(LocationModel).filter(
            LocationModel.id == location_id
        ).first()
        
        exists = location is not None
        logger.info(f"Location {location_id} exists: {exists}")
        return exists
    
    async def check_category_exists(self, category_id: int) -> bool:
        """Check if a category exists by ID."""
        logger.info(f"Checking if category {category_id} exists")
        
        category = self.session.query(CategoryModel).filter(
            CategoryModel.id == category_id
        ).first()
        
        exists = category is not None
        logger.info(f"Category {category_id} exists: {exists}")
        return exists 