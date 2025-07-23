"""FastAPI routes for recommendations."""
from typing import List
from fastapi import APIRouter, Depends
from ...application.use_cases.get_recommendations import GetRecommendationsUseCase
from ...application.use_cases.mark_as_reviewed import MarkAsReviewedUseCase
from ...application.dtos import MarkAsReviewedDTO
from .schemas import RecommendationResponseSchema, MarkAsReviewedSchema
from config.dependencies import (
    get_get_recommendations_use_case,
    get_mark_as_reviewed_use_case
)
from src.shared.logging.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/", response_model=List[RecommendationResponseSchema])
async def get_recommendations(
    use_case: GetRecommendationsUseCase = Depends(get_get_recommendations_use_case)
) -> List[RecommendationResponseSchema]:
    """Get location-category recommendations not reviewed in the last 30 days."""
    logger.info("Getting recommendations")
    
    # Execute use case
    results = await use_case.execute()
    
    logger.info(f"Retrieved {len(results)} recommendations")
    return results


@router.post("/mark-reviewed", status_code=200)
async def mark_as_reviewed(
    data: MarkAsReviewedSchema,
    use_case: MarkAsReviewedUseCase = Depends(get_mark_as_reviewed_use_case)
) -> dict:
    """Mark a location-category combination as reviewed."""
    logger.info(f"Marking location {data.location_id} - category {data.category_id} as reviewed")
    
    # Convert schema to DTO
    mark_dto = MarkAsReviewedDTO(
        location_id=data.location_id,
        category_id=data.category_id
    )
    
    # Execute use case
    await use_case.execute(mark_dto)
    
    logger.info(f"Successfully marked location {data.location_id} - category {data.category_id} as reviewed")
    return {"message": "Successfully marked as reviewed"} 