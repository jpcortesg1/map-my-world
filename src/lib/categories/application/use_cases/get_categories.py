"""Get categories use case."""
from typing import List, Optional
from ...domain.repositories import CategoryRepository
from ...domain.entities import Category
from src.shared.logging.logger import get_logger
from src.shared.exceptions.http_errors import InternalServerError

logger = get_logger(__name__)


class GetCategoriesUseCase:
    """Use case for getting categories with optional filtering and pagination."""
    
    def __init__(self, category_repository: CategoryRepository) -> None:
        self.category_repository = category_repository
    
    async def execute(
        self, 
        limit: Optional[int] = None,
        offset: int = 0,
        name_filter: Optional[str] = None
    ) -> List[Category]:
        """Execute the get categories use case with pagination and filtering."""
        logger.info(f"Getting categories: limit={limit}, offset={offset}, name_filter={name_filter}")
        
        try:
            categories = await self.category_repository.get_all(
                limit=limit,
                offset=offset,
                name_filter=name_filter
            )
            
            logger.info(f"Successfully retrieved {len(categories)} categories")
            return categories
            
        except Exception as e:
            logger.error(f"Error fetching categories: {str(e)}")
            raise InternalServerError(
                error="Failed to retrieve categories",
                details=[{"context": "database", "message": "Error querying categories"}]
            ) 