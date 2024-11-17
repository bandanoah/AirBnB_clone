#!/usr/bin/python3
import uuid
import datetime


class Basemodel:
    """ Defines Basemodel class with common attributes/methods."""
    def __init__(self):
        """ Initializes a new instance of Basemode."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at

    def __str__(self):
        """ Return a string representation of the instance. """
        return f"[{self.__class__.name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """ updates 'updated_at' attribute with current datetime."""
        self.updated_at = datetime.now()

    def to_dict(self):
        """ Return a dictionary representation of the instances."""
        result = self.__dict__.copy()
        result["__class__"] = self.__class__.name__
        result["created_at"] = self.created_at.isoformat()
        result["updated_at"] = self.updated_at.isoformat()
        return result
