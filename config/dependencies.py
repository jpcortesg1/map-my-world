"""Dependency injection configuration for Map My World API."""
from typing import Generator
from sqlalchemy.orm import Session
from dependency_injector import containers, providers
from config.database import get_db, SessionLocal
from src.lib.locations.infrastructure.orm.repositories import LocationRepositoryImpl
from src.lib.categories.infrastructure.orm.repositories import CategoryRepositoryImpl
from src.lib.recommendations.infrastructure.orm.repositories import RecommendationRepositoryImpl
from src.lib.locations.application.use_cases.create_location import CreateLocationUseCase
from src.lib.locations.application.use_cases.get_locations import GetLocationsUseCase
from src.lib.locations.application.use_cases.get_location_by_id import GetLocationByIdUseCase
from src.lib.categories.application.use_cases.create_category import CreateCategoryUseCase
from src.lib.categories.application.use_cases.get_categories import GetCategoriesUseCase
from src.lib.recommendations.application.use_cases.get_recommendations import GetRecommendationsUseCase
from src.lib.recommendations.application.use_cases.mark_as_reviewed import MarkAsReviewedUseCase


class Container(containers.DeclarativeContainer):
    """Dependency injection container."""
    
    # Configuration
    config = providers.Configuration()
    
    # Database
    db_session = providers.Singleton(SessionLocal)
    
    # Repositories
    location_repository = providers.Factory(
        LocationRepositoryImpl,
        session=db_session,
    )
    
    category_repository = providers.Factory(
        CategoryRepositoryImpl,
        session=db_session,
    )
    
    recommendation_repository = providers.Factory(
        RecommendationRepositoryImpl,
        session=db_session,
    )
    
    # Use Cases
    create_location_use_case = providers.Factory(
        CreateLocationUseCase,
        location_repository=location_repository,
    )
    
    get_locations_use_case = providers.Factory(
        GetLocationsUseCase,
        location_repository=location_repository,
    )
    
    get_location_by_id_use_case = providers.Factory(
        GetLocationByIdUseCase,
        location_repository=location_repository,
    )
    
    create_category_use_case = providers.Factory(
        CreateCategoryUseCase,
        category_repository=category_repository,
    )
    
    get_categories_use_case = providers.Factory(
        GetCategoriesUseCase,
        category_repository=category_repository,
    )
    
    get_recommendations_use_case = providers.Factory(
        GetRecommendationsUseCase,
        recommendation_repository=recommendation_repository,
    )
    
    mark_as_reviewed_use_case = providers.Factory(
        MarkAsReviewedUseCase,
        recommendation_repository=recommendation_repository,
    )


# Global container instance
container = Container()

# Initialize the container
# container.wire(
#     modules=[
#         "src.lib.locations.infrastructure.api.routes",
#         "src.lib.categories.infrastructure.api.routes", 
#         "src.lib.recommendations.infrastructure.api.routes"
#     ]
# )


def get_db_session() -> Generator[Session, None, None]:
    """Get database session dependency."""
    return get_db()


# Use case dependencies
def get_create_location_use_case() -> CreateLocationUseCase:
    """Get create location use case dependency."""
    return container.create_location_use_case()


def get_get_locations_use_case() -> GetLocationsUseCase:
    """Get get locations use case dependency."""
    return container.get_locations_use_case()


def get_get_location_by_id_use_case() -> GetLocationByIdUseCase:
    """Get get location by id use case dependency."""
    return container.get_location_by_id_use_case()


def get_create_category_use_case() -> CreateCategoryUseCase:
    """Get create category use case dependency."""
    return container.create_category_use_case()


def get_get_categories_use_case() -> GetCategoriesUseCase:
    """Get get categories use case dependency."""
    return container.get_categories_use_case()


def get_get_recommendations_use_case() -> GetRecommendationsUseCase:
    """Get get recommendations use case dependency."""
    return container.get_recommendations_use_case()


def get_mark_as_reviewed_use_case() -> MarkAsReviewedUseCase:
    """Get mark as reviewed use case dependency."""
    return container.mark_as_reviewed_use_case() 