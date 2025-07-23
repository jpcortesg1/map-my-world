"""Get recommendations use case."""
from typing import List
from ...domain.repositories import RecommendationRepository
from ...domain.services import RecommendationDomainService
from ..dtos import RecommendationResponseDTO
from src.shared.logging.logger import get_logger

logger = get_logger(__name__)


class GetRecommendationsUseCase:
    """Use case for getting location-category recommendations."""
    
    def __init__(self, recommendation_repository: RecommendationRepository) -> None:
        self.recommendation_repository = recommendation_repository
    
    async def execute(self) -> List[dict]:
        """Execute the get recommendations use case."""
        logger.info("Getting location-category recommendations")
        
        # Get unreviewed combinations from repository
        # The repository handles the optimized SQL query
        combinations = await self.recommendation_repository.get_unreviewed_combinations(limit=10)
        
        logger.info(f"Retrieved {len(combinations)} recommendations")
        return combinations 