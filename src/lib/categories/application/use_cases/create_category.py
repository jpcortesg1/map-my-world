"""Create category use case."""
from datetime import datetime
from ...domain.entities import Category
from ...domain.repositories import CategoryRepository
from ..dtos import CategoryCreateDTO, CategoryResponseDTO
from src.shared.exceptions.domain_errors import DuplicateCategoryError
from src.shared.logging.logger import get_logger

logger = get_logger(__name__)


class CreateCategoryUseCase:
    """Use case for creating a new category."""
    
    def __init__(self, category_repository: CategoryRepository) -> None:
        self.category_repository = category_repository
    
    async def execute(self, category_data: CategoryCreateDTO) -> CategoryResponseDTO:
        """Execute the create category use case."""
        logger.info(f"Creating category: {category_data.name}")
        
        # Check for duplicates
        exists = await self.category_repository.exists_by_name(category_data.name)
        
        if exists:
            logger.warning(f"Duplicate category found: {category_data.name}")
            raise DuplicateCategoryError(name=category_data.name)
        
        # Create domain entity
        now = datetime.utcnow()
        category = Category(
            id=None,  # Will be set by database
            name=category_data.name,
            description=category_data.description,
            created_at=now,
            updated_at=now
        )
        
        # Save to repository
        created_category = await self.category_repository.create(category)
        
        logger.info(f"Category created successfully: {created_category.id}")
        return CategoryResponseDTO.from_domain(created_category) 