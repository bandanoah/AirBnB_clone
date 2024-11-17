#!/usr/bin/python3
"""Module base_model

This Module contains a definition for BaseModel Class, which serves as a
base class for all other models in the project. It provides methods for
serializing objects, managing unique identifiers, and handling timestamps.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional

import models


class BaseModel:
    """BaseModel Class

    A base class for other models. It includes attributes and methods
    common to all derived classes.
    """

    def __init__(self, *args: Any, **kwargs: Optional[Dict[str, Any]]) -> None:
        """
        Initialize a new BaseModel instance.

        - Automatically assigns a unique identifier (`id`).
        - Sets the creation and update timestamps (`created_at`, `updated_at`).
        - Supports instantiation with keyword arguments to allow deserialization
          from dictionaries (e.g., when loading objects from storage).

        Args:
            *args: Variable-length argument list (not used here).
            **kwargs: A dictionary of key/value pairs for object initialization.
                      If provided, these are used to populate the instance.
        """
        self.id = str(uuid.uuid4())  # Assign a unique ID to the instance
        self.created_at = datetime.now()  # Timestamp when the instance is created
        self.updated_at = datetime.now()  # Timestamp when the instance was last updated

        if kwargs:
            # If keyword arguments are provided, populate instance attributes
            for k, v in kwargs.items():
                if k == "__class__":
                    # Ignore the class name attribute from the dictionary
                    continue
                elif k in ["created_at", "updated_at"]:
                    try:
                        # Convert ISO 8601 strings to datetime objects
                        setattr(self, k, datetime.fromisoformat(v))
                    except ValueError:
                        raise ValueError(f"Invalid datetime format for {k}: {v}")
                else:
                    # Set other attributes dynamically
                    setattr(self, k, v)
        else:
            # Register the instance in the storage system if no kwargs are provided
            models.storage.new(self)

    def save(self) -> None:
        """
        Save the instance to persistent storage.

        - Updates the `updated_at` timestamp to the current datetime.
        - Calls the storage engine's `save` method to persist changes.
        """
        self.updated_at = datetime.now()  # Update the modification timestamp
        models.storage.save()  # Persist changes using the storage engine

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the instance to a dictionary.

        - Serializes all attributes, including those with `datetime` values,
          by converting them to ISO 8601 strings.
        - Includes the class name (`__class__`) for identification during
          deserialization.

        Returns:
            A dictionary representation of the instance.
        """
        # Serialize instance attributes to a dictionary
        bs_dict = {
            k: (v.isoformat() if isinstance(v, datetime) else v)
            for (k, v) in self.__dict__.items()
        }
        bs_dict["__class__"] = self.__class__.__name__  # Add the class name
        return bs_dict

    def __str__(self) -> str:
        """
        Provide a human-readable string representation of the instance.

        Returns:
            A string in the format:
            "[<class name>] (<id>) <instance dictionary>"
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

