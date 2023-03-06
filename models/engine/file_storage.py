#!/usr/bin/python3
"""File storage engine module."""
import json


class FileStorage:
    """Serialize data and save it as json, also deserialize
    json and create objects.

    Args:
        __file_path: string - path to the JSON file (ex: file.json)
        __objects: dictionary - empty but will store all objects
        by <class name>.id (ex: to store a BaseModel object with id=12121212,
        the key will be BaseModel.12121212).
    """
    __file_path: str = "file.json"
    __objects: dict = dict()

    def all(self):
        """Returns the dictionary objects <__objects>."""
        return self.__objects

    def new(self, obj):
        """ Set in the object in the __object dictionary with the kay
        which is a combination of the object class and the id
        example BaseModel.121212
        obj: instance object to serialize
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serialize and save the object to a json file
        specified by __file_path
        """
        for k, v in self.__objects.items():
            try:
                self.__objects[k] = v.to_dict()
            except AttributeError as e:
                pass

        with open(self.__file_path, 'w', encoding='utf-8') as f:
            json.dump(self.__objects, f)

    def reload(self):
        """Deserializes the JSON file to __objects (only if the JSON file (__file_path) exists
        otherwise, do nothing. If the file doesn’t exist, no exception should be raised).
        """

        try:
            with open(self.__file_path, 'r', encoding='utf-8') as f:
                self.__objects = json.loads(f.read())
        except (Exception):
            pass
