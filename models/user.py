#!/usr/bin/python3
"""Module base_model

This module contains a definition for the User class,
which represents a user in the application.
"""

from models.base_model import BaseModel


class User(BaseModel):
    """A class that represents a user.

    Inherits from:
        BaseModel: Provides core attributes and methods for persistent models.

    Attributes:
        email (str): The email of the user.
        password (str): The password of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
    """

    email: str = ""       # The user's email address
    password: str = ""    # The user's password (should be hashed in real implementations)
    first_name: str = ""  # The user's first name
    last_name: str = ""   # The user's last name

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize a User instance.

        Args:
            *args: Variable length argument list (not used here).
            **kwargs: Dictionary of key/value pairs for initialization.
                      If provided, these are passed to the BaseModel.
        """
        super().__init__(*args, **kwargs)

    def validate_attributes(self) -> bool:
        """
        Validate the attributes of the User instance.

        Ensures that the `email` and `password` are non-empty strings.

        Returns:
            bool: True if all required attributes are valid, False otherwise.
        """
        if not isinstance(self.email, str) or not self.email.strip():
            return False
        if not isinstance(self.password, str) or not self.password.strip():
            return False
        return True

    def to_dict(self) -> dict:
        """
        Convert the instance to a dictionary.

        Overrides BaseModel's `to_dict` to exclude sensitive attributes.

        Returns:
            dict: A dictionary representation of the User instance, excluding the password.
        """
        user_dict = super().to_dict()
        user_dict.pop("password", None)  # Exclude the password field
        return user_dict

