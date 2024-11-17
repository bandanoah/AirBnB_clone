#!/usr/bin/python3
"""Module file_storage

This module contains a definition for the FileStorage class,
which handles object persistence using a JSON file.
"""

import importlib
import json
import os
import re


class FileStorage:
    """FileStorage Class

    Handles serialization and deserialization of objects to and from a JSON file.

    Attributes:
        __file_path (str): Path to the JSON file used for persistence.
        __objects (dict): A dictionary of instantiated objects, stored as
                          "<class_name>.<id>": object.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Retrieve all objects currently in storage.

        Returns:
            dict: The dictionary of stored objects.
        """
        return self.__objects

    def new(self, obj):
        """
        Add a new object to storage.

        Args:
            obj: The object to add, must have `id` and `__class__.__name__` attributes.
        """
        if not hasattr(obj, 'id') or not hasattr(obj, '__class__'):
            raise AttributeError("Object must have 'id' and '__class__' attributes.")
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """
        Serialize all objects in storage to the JSON file defined by `__file_path`.

        Converts objects to dictionaries using their `to_dict` method.
        """
        try:
            with open(self.__file_path, 'w') as f:
                json.dump({k: v.to_dict() for k, v in self.__objects.items()}, f)
        except Exception as e:
            raise IOError(f"Error saving to file {self.__file_path}: {e}")

    def reload(self):
        """
        Deserialize the JSON file into objects and load them into storage.

        If the file does not exist or is empty, no action is taken.
        """
        if os.path.isfile(self.__file_path) and os.path.getsize(self.__file_path) > 0:
            try:
                with open(self.__file_path, 'r') as f:
                    # Convert JSON objects back to class instances
                    self.__objects = {k: self.get_class(k.split(".")[0])(**v)
                                      for k, v in json.load(f).items()}
            except (json.JSONDecodeError, FileNotFoundError) as e:
                raise ValueError(f"Error reading from file {self.__file_path}: {e}")

    def get_class(self, name):
        """
        Retrieve a class from the `models` module using its name.

        Args:
            name (str): The name of the class to retrieve.

        Returns:
            type: The class object.

        Raises:
            ImportError: If the class module cannot be found.
            AttributeError: If the class is not found in the module.
        """
        try:
            # Convert CamelCase class name to snake_case module name
            sub_module = re.sub(r'(?!^)([A-Z]+)', r'_\1', name).lower()
            module = importlib.import_module(f"models.{sub_module}")
            return getattr(module, name)
        except ImportError as e:
            raise ImportError(f"Module for class '{name}' could not be imported: {e}")
        except AttributeError as e:
            raise AttributeError(f"Class '{name}' not found in its module: {e}")

