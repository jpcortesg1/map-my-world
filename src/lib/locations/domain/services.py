"""Domain services for locations."""
from typing import List
from .entities import Location
from .value_objects import Coordinates


class LocationDomainService:
    """Domain service for location operations."""
    
    @staticmethod
    def validate_coordinates(longitude: float, latitude: float) -> Coordinates:
        """Validate and create coordinates."""
        return Coordinates(longitude=longitude, latitude=latitude)
    
    @staticmethod
    def calculate_distance(location1: Location, location2: Location) -> float:
        """Calculate distance between two locations using Haversine formula."""
        import math
        
        # Convert to radians
        lat1, lon1 = math.radians(location1.latitude), math.radians(location1.longitude)
        lat2, lon2 = math.radians(location2.latitude), math.radians(location2.longitude)
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Earth's radius in kilometers
        r = 6371
        
        return c * r 