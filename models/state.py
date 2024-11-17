#!/usr/bin/python3
"""Module base_model

This module contains a definition for the State class,
which represents a geographical or administrative state.
"""

from models.base_model import BaseModel


class State(BaseModel):
    """A class that represents a state.

    Inherits from:
        BaseModel: Provides core attributes and methods for persistent models.

    Attributes:
        name (str): The name of the state.
    """

    name: str = ""  # The name of the state, initialized as an empty string

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize a State instance.

        Args:
            *args: Variable length argument list (not used here).
            **kwargs: Dictionary of key/value pairs for initialization.
                      If provided, these are passed to the BaseModel.
        """
        super().__init__(*args, **kwargs)

    def validate_attributes(self) -> bool:
        """
        Validate the attributes of the State instance.

        Ensures that the `name` attribute is a non-empty string.

        Returns:
            bool: True if the name is valid, False otherwise.
        """
        return isinstance(self.name, str) and len(self.name.strip()) > 0

