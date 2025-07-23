#!/usr/bin/env python3
"""Script to initialize the database with sample data."""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import create_tables, SessionLocal
from src.lib.locations.infrastructure.orm.models import LocationModel
from src.lib.categories.infrastructure.orm.models import CategoryModel
# Import needed for SQLAlchemy to register the model and create the table
import src.lib.recommendations.infrastructure.orm.models  # type: ignore # noqa: F401
from src.shared.logging.logger import get_logger

logger = get_logger(__name__)


def create_sample_data():
    """Create sample data for testing."""
    logger.info("Creating sample data...")
    
    # Create database session
    session = SessionLocal()
    
    try:
        # Create sample categories
        categories = [
            CategoryModel(
                name="Restaurants",
                description="Places to eat and dine"
            ),
            CategoryModel(
                name="Parks",
                description="Public parks and recreational areas"
            ),
            CategoryModel(
                name="Museums",
                description="Cultural and educational institutions"
            ),
            CategoryModel(
                name="Shopping Centers",
                description="Retail and shopping destinations"
            ),
            CategoryModel(
                name="Hotels",
                description="Accommodation and lodging"
            ),
        ]
        
        for category in categories:
            session.add(category)
        
        session.commit()
        logger.info(f"Created {len(categories)} categories")
        
        # Create sample locations
        locations = [
            LocationModel(
                name="Central Park",
                longitude=-73.935242,
                latitude=40.782865,
                description="A large urban park in Manhattan, New York City"
            ),
            LocationModel(
                name="Times Square",
                longitude=-73.9855,
                latitude=40.7580,
                description="Major commercial intersection and tourist destination"
            ),
            LocationModel(
                name="Empire State Building",
                longitude=-73.9857,
                latitude=40.7484,
                description="Iconic skyscraper and observation deck"
            ),
            LocationModel(
                name="Brooklyn Bridge",
                longitude=-73.9969,
                latitude=40.7061,
                description="Historic suspension bridge connecting Manhattan and Brooklyn"
            ),
            LocationModel(
                name="Statue of Liberty",
                longitude=-74.0445,
                latitude=40.6892,
                description="Famous monument and symbol of freedom"
            ),
            LocationModel(
                name="Metropolitan Museum of Art",
                longitude=-73.9632,
                latitude=40.7794,
                description="World-famous art museum"
            ),
            LocationModel(
                name="Broadway",
                longitude=-73.9857,
                latitude=40.7589,
                description="Famous theater district and entertainment hub"
            ),
            LocationModel(
                name="Rockefeller Center",
                longitude=-73.9787,
                latitude=40.7587,
                description="Complex of commercial buildings and entertainment venues"
            ),
        ]
        
        for location in locations:
            session.add(location)
        
        session.commit()
        logger.info(f"Created {len(locations)} locations")
        
        logger.info("Sample data created successfully!")
        
    except Exception as e:
        logger.error(f"Error creating sample data: {e}")
        session.rollback()
        raise
    finally:
        session.close()


def main():
    """Main function to initialize the database."""
    logger.info("Initializing database...")
    
    # Create tables
    create_tables()
    logger.info("Database tables created")
    
    # Create sample data
    create_sample_data()
    
    logger.info("Database initialization completed successfully!")


if __name__ == "__main__":
    main() 