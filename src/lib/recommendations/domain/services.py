"""Domain services for recommendations."""
from typing import List
from datetime import datetime, timedelta
from .entities import LocationCategoryReview


class RecommendationDomainService:
    """Domain service for recommendation operations."""
    
    @staticmethod
    def filter_recent_reviews(reviews: List[LocationCategoryReview], days: int = 30) -> List[LocationCategoryReview]:
        """Filter reviews to only include those from the last N days."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return [
            review for review in reviews 
            if review.reviewed_at and review.reviewed_at > cutoff_date
        ]
    
    @staticmethod
    def prioritize_unreviewed(reviews: List[LocationCategoryReview]) -> List[LocationCategoryReview]:
        """Prioritize never-reviewed combinations over recently reviewed ones."""
        # Sort by reviewed_at (None first, then oldest first)
        return sorted(reviews, key=lambda x: (x.reviewed_at is not None, x.reviewed_at or datetime.min))
    
    @staticmethod
    def limit_results(reviews: List[LocationCategoryReview], limit: int = 10) -> List[LocationCategoryReview]:
        """Limit the number of results."""
        return reviews[:limit] 