#!/usr/bin/python3
"""
Base Model module.

Define all common attributes and methods of other classes
"""
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Base Model abstract class."""

    def __init__(self, *args, **kwargs):
        """Basemodel constructor.

        Args:
            args (list): list of arguments passed
            kwargs (dict): keyword arguments
            id: string - assign with an uuid when an instance is created.
            created_at: datetime - assign with the current datetime when
             an instance is created.
            updated_at: datetime - assign with the current datetime when an
             instance is created and it will be updated every time you change.
        """
        if kwargs is not None and len(kwargs) != 0:
            for k in kwargs:
                if k == '__class__':
                    continue
                elif k in ['created_at', 'updated_at']:
                    self.__setattr__(k, datetime.fromisoformat(kwargs[k]))
                else:
                    self.__setattr__(k, kwargs[k])
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at

    def save(self):
        """Update instance attributes and write the timestamp to
        the updated_at attribute."""
        self.updated_at = datetime.now()

    def to_dict(self):
        """Dicttionary representation of instance attributes."""
        result = self.__dict__.copy()
        result['__class__'] = self.__class__.__name__
        result['created_at'] = self.created_at.isoformat()
        result['updated_at'] = self.updated_at.isoformat()
        return result

    def __str__(self) -> str:
        """Readable representation of the class."""
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)
