import os
import unittest

from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorageTest(unittest.TestCase):
    """ Test the FileStorage class """
    s_test = storage
    s_test._FileStorage__file_path = "test.json"

    @classmethod
    def setUpClass(cls):
        """ class before the tests """

        objs = cls.s_test._FileStorage__objects.copy()
        for key in objs.keys():
            del cls.s_test._FileStorage__objects[key]

        try:
            os.remove("test.json")
        except FileNotFoundError:
            pass

    def test_storage1(self):
        """ test file storage """

        self.assertTrue(type(self.s_test._FileStorage__file_path) is str)
        self.assertTrue(type(self.s_test._FileStorage__objects) is dict)

    def test_storage2(self):
        """ test file storage """

        self.assertEqual(self.s_test._FileStorage__file_path, "test.json")
        self.assertEqual(self.s_test._FileStorage__objects, {})

    def test_storage_new(self):
        """ Test the new method """

        b1 = BaseModel()
        u1 = User()
        s1 = State()
        c1 = City()
        a1 = Amenity()
        p1 = Place()
        r1 = Review()

        objs = [b1, u1, s1, c1, a1, p1, r1]
        self.assertEqual(len(self.s_test._FileStorage__objects), 7)

        i = 0
        for key, val in self.s_test._FileStorage__objects.items():
            obj_key = "{}.{}".format(objs[i].__class__.__name__, objs[i].id)
            self.assertEqual(obj_key, key)
            self.assertTrue(val is objs[i])
            i += 1

    def test_storage_new_more_args(self):
        """ Test the new method with more args """

        with self.assertRaises(TypeError):
            self.s_test.new("b1", "u1")

    def test_storage_new_less_args(self):
        """ Test the new method with less args """

        with self.assertRaises(TypeError):
            self.s_test.new()

    def test_storage_all(self):
        """ Test the all method """

        all_objs = self.s_test.all()

        self.assertTrue(type(all_objs) is dict)

        for key, val in all_objs.items():
            self.assertTrue(key in self.s_test._FileStorage__objects)
            self.assertEqual(val, self.s_test._FileStorage__objects[key])

        self.assertTrue(all_objs is self.s_test._FileStorage__objects)

    def test_storage_all_args(self):
        """ test the all method with args """

        with self.assertRaises(TypeError):
            all_objs = self.s_test.all("12")

    def test_storage_save_and_reload(self):
        """ test the save method and reload """

        self.assertFalse(os.path.exists(self.s_test._FileStorage__file_path))

        self.s_test.save()

        self.assertTrue(os.path.exists(self.s_test._FileStorage__file_path))
        self.assertTrue(os.path.isfile(self.s_test._FileStorage__file_path))

        obj_dict = self.s_test._FileStorage__objects.copy()
        for key, val in obj_dict.items():
            del self.s_test._FileStorage__objects[key]

        self.assertEqual(len(self.s_test._FileStorage__objects), 0)
        self.assertEqual(len(self.s_test._FileStorage__objects), 0)

        self.s_test.reload()
        FileStorageTest.s_objs = self.s_test._FileStorage__objects

        self.assertEqual(len(self.s_test._FileStorage__objects), 7)
        self.assertEqual(len(self.s_test._FileStorage__objects), 7)
        models = [BaseModel, User, State, City, Amenity, Place, Review]
        i = 0
        for key, val in self.s_test._FileStorage__objects.items():
            self.assertTrue(type(val) is models[i])
            i += 1

    def test_storage_save_args(self):
        """ test the save method with args """

        with self.assertRaises(TypeError):
            self.s_test.save("hey")

    def test_storage_reload_args(self):
        """ test the reload method with args """

        with self.assertRaises(TypeError):
            self.s_test.save(102895)

    def test_instance_add_with_kwargs(self):
        bm = BaseModel()
        from_json = bm.to_dict()
        print(self.s_test._FileStorage__objects)
        self.assertIn(".".join([
            "BaseModel", bm.id
        ]), storage.all())
        del storage._FileStorage__objects[".".join([
            "BaseModel", bm.id
        ])]
        res = BaseModel(**from_json)
        self.assertNotIn(".".join([
            "BaseModel", bm.id
        ]), storage.all())

    @classmethod
    def tearDownClass(cls):
        """ calls after the tests """

        objs = cls.s_test._FileStorage__objects.copy()
        for key in objs.keys():
            del cls.s_test._FileStorage__objects[key]

        cls.s_test._FileStorage__objects = {}
        try:
            os.remove("test.json")
        except FileNotFoundError:
            pass
