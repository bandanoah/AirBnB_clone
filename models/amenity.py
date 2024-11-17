#!/usr/bin/python3
"""Module base_model

This module contains a definition for the Amenity class,
which represents a type of amenity in the application.
"""

from models.base_model import BaseModel


class Amenity(BaseModel):
    """A class that represents an amenity.

    Inherits from:
        BaseModel: Provides core attributes and methods for persistent models.

    Attributes:
        name (str): The name of the amenity. Default is an empty string.
    """

    name: str = ""

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize an Amenity instance.

        Args:
            *args: Variable length argument list (not used here).
            **kwargs: Dictionary of key/value pairs for initialization.
                      If provided, these are passed to the BaseModel.
        """
        super().__init__(*args, **kwargs)

    def validate_name(self) -> bool:
        """
        Validate the `name` attribute to ensure it meets requirements.

        Returns:
            bool: True if `name` is valid, False otherwise.
        """
        return isinstance(self.name, str) and len(self.name.strip()) > 0

