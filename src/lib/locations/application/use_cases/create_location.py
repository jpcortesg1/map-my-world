"""Create location use case."""
from datetime import datetime
from typing import Protocol
from ...domain.entities import Location
from ...domain.repositories import LocationRepository
from ...domain.services import LocationDomainService
from ...domain.value_objects import Coordinates
from ..dtos import LocationCreateDTO, LocationResponseDTO
from src.shared.exceptions.domain_errors import DuplicateLocationError
from src.shared.logging.logger import get_logger

logger = get_logger(__name__)


class CreateLocationUseCase:
    """Use case for creating a new location."""
    
    def __init__(self, location_repository: LocationRepository) -> None:
        self.location_repository = location_repository
    
    async def execute(self, location_data: LocationCreateDTO) -> LocationResponseDTO:
        """Execute the create location use case."""
        logger.info(f"Creating location: {location_data.name}")
        
        # Validate coordinates
        coordinates = LocationDomainService.validate_coordinates(
            longitude=location_data.longitude,
            latitude=location_data.latitude
        )
        
        # Check for duplicates
        exists = await self.location_repository.exists_by_name_and_coordinates(
            name=location_data.name,
            longitude=location_data.longitude,
            latitude=location_data.latitude
        )
        
        if exists:
            logger.warning(f"Duplicate location found: {location_data.name}")
            raise DuplicateLocationError(
                name=location_data.name,
                longitude=location_data.longitude,
                latitude=location_data.latitude
            )
        
        # Create domain entity
        now = datetime.utcnow()
        location = Location(
            id=None,  # Will be set by database
            coordinates=coordinates,
            name=location_data.name,
            description=location_data.description,
            created_at=now,
            updated_at=now
        )
        
        # Save to repository
        created_location = await self.location_repository.create(location)
        
        logger.info(f"Location created successfully: {created_location.id}")
        return LocationResponseDTO.from_domain(created_location) 