"""FastAPI routes for locations."""
from typing import List
from fastapi import APIRouter, Depends
from ...application.use_cases.create_location import CreateLocationUseCase
from ...application.use_cases.get_locations import GetLocationsUseCase
from ...application.use_cases.get_location_by_id import GetLocationByIdUseCase
from ...application.dtos import LocationCreateDTO
from .schemas import LocationCreateSchema, LocationResponseSchema, LocationQueryParams
from config.dependencies import (
    get_create_location_use_case,
    get_get_locations_use_case,
    get_get_location_by_id_use_case
)
from src.shared.logging.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/locations", tags=["locations"])


@router.post("/", response_model=LocationResponseSchema, status_code=201)
async def create_location(
    location_data: LocationCreateSchema,
    use_case: CreateLocationUseCase = Depends(get_create_location_use_case)
) -> LocationResponseSchema:
    """Create a new location."""
    logger.info(f"Creating location: {location_data.name}")
    
    # Convert schema to DTO
    location_dto = LocationCreateDTO(
        name=location_data.name,
        longitude=location_data.longitude,
        latitude=location_data.latitude,
        description=location_data.description
    )
    
    # Execute use case
    result = await use_case.execute(location_dto)
    
    logger.info(f"Location created successfully: {result.id}")
    return LocationResponseSchema.from_domain(result)


@router.get("/", response_model=List[LocationResponseSchema])
async def get_locations(
    query_params: LocationQueryParams = Depends(),
    use_case: GetLocationsUseCase = Depends(get_get_locations_use_case)
) -> List[LocationResponseSchema]:
    """Get locations with optional pagination and filtering."""
    logger.info(f"Getting locations with params: limit={query_params.limit}, offset={query_params.offset}, name={query_params.name}")
    
    # Execute use case
    locations = await use_case.execute(
        limit=query_params.limit,
        offset=query_params.offset,
        name_filter=query_params.name
    )
    
    logger.info(f"Returned {len(locations)} locations")
    return [LocationResponseSchema.from_domain(location) for location in locations]


@router.get("/{location_id}", response_model=LocationResponseSchema)
async def get_location(
    location_id: int,
    use_case: GetLocationByIdUseCase = Depends(get_get_location_by_id_use_case)
) -> LocationResponseSchema:
    """Get a specific location by ID."""
    logger.info(f"Getting location: {location_id}")
    
    # Execute use case
    result = await use_case.execute(location_id)
    
    logger.info(f"Location returned successfully: {location_id}")
    return LocationResponseSchema.from_domain(result) 