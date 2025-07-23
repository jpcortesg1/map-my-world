"""Mark as reviewed use case."""
from ...domain.repositories import RecommendationRepository
from ..dtos import MarkAsReviewedDTO
from src.shared.logging.logger import get_logger
from src.shared.exceptions.domain_errors import LocationNotFoundError, CategoryNotFoundError

logger = get_logger(__name__)


class MarkAsReviewedUseCase:
    """Use case for marking a location-category combination as reviewed."""
    
    def __init__(self, recommendation_repository: RecommendationRepository) -> None:
        self.recommendation_repository = recommendation_repository
    
    async def execute(self, data: MarkAsReviewedDTO) -> None:
        """Execute the mark as reviewed use case."""
        logger.info(f"Marking location {data.location_id} - category {data.category_id} as reviewed")
        
        # Validate that location and category exist
        await self._validate_location_and_category(data.location_id, data.category_id)
        
        # Mark as reviewed in repository
        await self.recommendation_repository.mark_as_reviewed(
            location_id=data.location_id,
            category_id=data.category_id
        )
        
        logger.info(f"Successfully marked location {data.location_id} - category {data.category_id} as reviewed")
    
    async def _validate_location_and_category(self, location_id: int, category_id: int) -> None:
        """Validate that both location and category exist."""
        # Check if location exists
        location_exists = await self.recommendation_repository.check_location_exists(location_id)
        if not location_exists:
            raise LocationNotFoundError(location_id)
        
        # Check if category exists
        category_exists = await self.recommendation_repository.check_category_exists(category_id)
        if not category_exists:
            raise CategoryNotFoundError(category_id) 