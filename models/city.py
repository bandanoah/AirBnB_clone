#!/usr/bin/python3
"""Module base_model

This module contains a definition for the City class,
which represents a city in the application.
"""

from models.base_model import BaseModel


class City(BaseModel):
    """A class that represents a city.

    Inherits from:
        BaseModel: Provides core attributes and methods for persistent models.

    Attributes:
        state_id (str): The unique identifier for the state the city belongs to.
        name (str): The name of the city.
    """

    state_id: str = ""  # State ID associated with this city
    name: str = ""      # Name of the city

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize a City instance.

        Args:
            *args: Variable length argument list (not used here).
            **kwargs: Dictionary of key/value pairs for initialization.
                      If provided, these are passed to the BaseModel.
        """
        super().__init__(*args, **kwargs)

    def validate_attributes(self) -> bool:
        """
        Validate the attributes `state_id` and `name`.

        Ensures that both attributes are non-empty strings.

        Returns:
            bool: True if both attributes are valid, False otherwise.
        """
        if not isinstance(self.state_id, str) or not self.state_id.strip():
            return False
        if not isinstance(self.name, str) or not self.name.strip():
            return False
        return True

