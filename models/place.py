#!/usr/bin/python3
"""Module base_model

This module contains a definition for the Place class,
which represents a place (e.g., property) in the application.
"""

from models.base_model import BaseModel
from typing import List


class Place(BaseModel):
    """A class that represents a place.

    Inherits from:
        BaseModel: Provides core attributes and methods for persistent models.

    Attributes:
        city_id (str): The City id the place is associated with.
        user_id (str): The User id of the owner/creator of the place.
        name (str): The name of the place.
        description (str): A brief description of the place.
        number_rooms (int): The number of rooms in the place.
        number_bathrooms (int): The number of bathrooms in the place.
        max_guest (int): The maximum number of guests the place can accommodate.
        price_by_night (int): The price per night to rent the place.
        latitude (float): The geographical latitude of the place.
        longitude (float): The geographical longitude of the place.
        amenity_ids (list): A list of Amenity ids linked to the place.
    """

    city_id: str = ""           # ID of the city the place belongs to
    user_id: str = ""           # ID of the user who owns or created the place
    name: str = ""              # Name of the place
    description: str = ""       # Description of the place
    number_rooms: int = 0       # Number of rooms in the place
    number_bathrooms: int = 0   # Number of bathrooms in the place
    max_guest: int = 0          # Maximum number of guests allowed
    price_by_night: int = 0     # Price per night for renting the place
    latitude: float = 0.0       # Latitude for geographical location
    longitude: float = 0.0      # Longitude for geographical location
    amenity_ids: List[str] = [] # List of Amenity IDs associated with the place

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize a Place instance.

        Args:
            *args: Variable length argument list (not used here).
            **kwargs: Dictionary of key/value pairs for initialization.
                      If provided, these are passed to the BaseModel.
        """
        super().__init__(*args, **kwargs)

    def validate_attributes(self) -> bool:
        """
        Validate the attributes of the Place instance.

        Ensures that numerical values are non-negative and that
        latitude and longitude are within valid geographical ranges.

        Returns:
            bool: True if all attributes are valid, False otherwise.
        """
        if not isinstance(self.number_rooms, int) or self.number_rooms < 0:
            return False
        if not isinstance(self.number_bathrooms, int) or self.number_bathrooms < 0:
            return False
        if not isinstance(self.max_guest, int) or self.max_guest < 0:
            return False
        if not isinstance(self.price_by_night, int) or self.price_by_night < 0:
            return False
        if not (-90 <= self.latitude <= 90):
            return False
        if not (-180 <= self.longitude <= 180):
            return False
        return True

