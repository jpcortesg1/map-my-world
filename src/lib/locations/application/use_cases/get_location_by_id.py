"""Get location by ID use case."""
from ...domain.repositories import LocationRepository
from ..dtos import LocationResponseDTO
from src.shared.exceptions.domain_errors import LocationNotFoundError
from src.shared.logging.logger import get_logger

logger = get_logger(__name__)


class GetLocationByIdUseCase:
    """Use case for getting a location by ID."""
    
    def __init__(self, location_repository: LocationRepository) -> None:
        self.location_repository = location_repository
    
    async def execute(self, location_id: int) -> LocationResponseDTO:
        """Execute the get location by ID use case."""
        logger.info(f"Getting location by ID: {location_id}")
        
        location = await self.location_repository.get_by_id(location_id)
        
        if not location:
            logger.warning(f"Location not found: {location_id}")
            raise LocationNotFoundError(location_id)
        
        logger.info(f"Location retrieved successfully: {location_id}")
        return LocationResponseDTO.from_domain(location) 