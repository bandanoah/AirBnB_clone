#!/usr/bin/python3
"""Module base_model

This module contains a definition for the Review class,
which represents a review for a place in the application.
"""

from models.base_model import BaseModel


class Review(BaseModel):
    """A class that represents a review.

    Inherits from:
        BaseModel: Provides core attributes and methods for persistent models.

    Attributes:
        place_id (str): The ID of the place being reviewed.
        user_id (str): The ID of the user who wrote the review.
        text (str): The content of the review.
    """

    place_id: str = ""  # The ID of the associated place
    user_id: str = ""   # The ID of the user who created the review
    text: str = ""      # The actual text content of the review

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize a Review instance.

        Args:
            *args: Variable length argument list (not used here).
            **kwargs: Dictionary of key/value pairs for initialization.
                      If provided, these are passed to the BaseModel.
        """
        super().__init__(*args, **kwargs)

    def validate_attributes(self) -> bool:
        """
        Validate the attributes of the Review instance.

        Ensures that all required fields are non-empty strings.

        Returns:
            bool: True if all attributes are valid, False otherwise.
        """
        if not isinstance(self.place_id, str) or not self.place_id.strip():
            return False
        if not isinstance(self.user_id, str) or not self.user_id.strip():
            return False
        if not isinstance(self.text, str) or not self.text.strip():
            return False
        return True

