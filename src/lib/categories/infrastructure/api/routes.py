"""FastAPI routes for categories."""
from typing import List
from fastapi import APIRouter, Depends
from ...application.use_cases.create_category import CreateCategoryUseCase
from ...application.use_cases.get_categories import GetCategoriesUseCase
from ...application.dtos import CategoryCreateDTO
from .schemas import CategoryCreateSchema, CategoryResponseSchema, CategoryQueryParams
from config.dependencies import (
    get_create_category_use_case,
    get_get_categories_use_case
)
from src.shared.logging.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryResponseSchema, status_code=201)
async def create_category(
    category_data: CategoryCreateSchema,
    use_case: CreateCategoryUseCase = Depends(get_create_category_use_case)
) -> CategoryResponseSchema:
    """Create a new category."""
    logger.info(f"Creating category: {category_data.name}")
    
    # Convert schema to DTO
    category_dto = CategoryCreateDTO(
        name=category_data.name,
        description=category_data.description
    )
    
    # Execute use case
    result = await use_case.execute(category_dto)
    
    logger.info(f"Category created successfully: {result.id}")
    return CategoryResponseSchema.from_domain(result)


@router.get("/", response_model=List[CategoryResponseSchema])
async def get_categories(
    query_params: CategoryQueryParams = Depends(),
    use_case: GetCategoriesUseCase = Depends(get_get_categories_use_case)
) -> List[CategoryResponseSchema]:
    """Get categories with optional pagination and filtering."""
    logger.info(f"Getting categories with params: limit={query_params.limit}, offset={query_params.offset}, name={query_params.name}")
    
    # Execute use case
    categories = await use_case.execute(
        limit=query_params.limit,
        offset=query_params.offset,
        name_filter=query_params.name
    )
    
    logger.info(f"Returned {len(categories)} categories")
    return [CategoryResponseSchema.from_domain(category) for category in categories] 