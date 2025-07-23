"""Get locations use case."""
from typing import List, Optional
from ...domain.repositories import LocationRepository
from ...domain.entities import Location
from src.shared.logging.logger import get_logger
from src.shared.exceptions.http_errors import InternalServerError

logger = get_logger(__name__)


class GetLocationsUseCase:
    """Use case for getting locations with optional filtering and pagination."""
    
    def __init__(self, location_repository: LocationRepository) -> None:
        self.location_repository = location_repository
    
    async def execute(
        self, 
        limit: Optional[int] = None,
        offset: int = 0,
        name_filter: Optional[str] = None
    ) -> List[Location]:
        """Execute the get locations use case with pagination and filtering."""
        logger.info(f"Getting locations: limit={limit}, offset={offset}, name_filter={name_filter}")
        
        try:
            locations = await self.location_repository.get_all(
                limit=limit,
                offset=offset,
                name_filter=name_filter
            )
            
            logger.info(f"Successfully retrieved {len(locations)} locations")
            return locations
            
        except Exception as e:
            logger.error(f"Error fetching locations: {str(e)}")
            raise InternalServerError(
                error="Failed to retrieve locations",
                details=[{"context": "database", "message": "Error querying locations"}]
            ) 