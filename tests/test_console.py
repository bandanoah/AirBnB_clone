#!/usr/bin/python3
"""Module test_console

This module contains tests for the HBNBCommand class.
"""

import os
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel


class TestConsole(unittest.TestCase):
    """Test suite for the HBNBCommand class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up a shared test console."""
        cls.cmd = HBNBCommand()

    @classmethod
    def tearDownClass(cls) -> None:
        """Remove any temporary files created during tests."""
        if os.path.exists('file.json'):
            os.remove('file.json')

    def setUp(self) -> None:
        """Ensure a clean state before each test."""
        storage._FileStorage__objects = {}

    def test_create_missing_class_name(self):
        """Test error when no class name is provided to create."""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create')
            self.assertEqual("** class name missing **\n", output.getvalue())

    def test_create_invalid_class(self):
        """Test error when an invalid class name is provided."""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create InvalidClass')
            self.assertEqual("** class doesn't exist **\n", output.getvalue())

    def test_create_valid_class(self):
        """Test successful creation of a valid class instance."""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('create BaseModel')
            instance_id = output.getvalue().strip()
            self.assertTrue(instance_id)
            self.assertIn(f"BaseModel.{instance_id}", storage.all())

    def test_show_missing_class_name(self):
        """Test error when no class name is provided to show."""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('show')
            self.assertEqual("** class name missing **\n", output.getvalue())

    def test_show_non_existent_instance(self):
        """Test error when trying to show a non-existent instance."""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('show BaseModel invalid_id')
            self.assertEqual("** no instance found **\n", output.getvalue())

    def test_show_valid_instance(self):
        """Test successful retrieval of an existing instance."""
        obj = BaseModel()
        obj.save()
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd(f'show BaseModel {obj.id}')
            self.assertIn(f"[BaseModel] ({obj.id})", output.getvalue())

    def test_destroy_missing_class_name(self):
        """Test error when no class name is provided to destroy."""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('destroy')
            self.assertEqual("** class name missing **\n", output.getvalue())

    def test_destroy_valid_instance(self):
        """Test successful deletion of an existing instance."""
        obj = BaseModel()
        obj.save()
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd(f'destroy BaseModel {obj.id}')
            self.assertNotIn(f"BaseModel.{obj.id}", storage.all())

    def test_all_no_class_filter(self):
        """Test retrieval of all instances without a class filter."""
        obj1 = BaseModel()
        obj2 = BaseModel()
        obj1.save()
        obj2.save()
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('all')
            self.assertIn(f"[BaseModel] ({obj1.id})", output.getvalue())
            self.assertIn(f"[BaseModel] ({obj2.id})", output.getvalue())

    def test_all_with_class_filter(self):
        """Test retrieval of all instances of a specific class."""
        obj1 = BaseModel()
        obj2 = BaseModel()
        obj1.save()
        obj2.save()
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('all BaseModel')
            self.assertIn(f"[BaseModel] ({obj1.id})", output.getvalue())
            self.assertIn(f"[BaseModel] ({obj2.id})", output.getvalue())

    def test_update_missing_class_name(self):
        """Test error when no class name is provided to update."""
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('update')
            self.assertEqual("** class name missing **\n", output.getvalue())

    def test_update_missing_attribute_name(self):
        """Test error when no attribute name is provided to update."""
        obj = BaseModel()
        obj.save()
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd(f'update BaseModel {obj.id}')
            self.assertIn("** attribute name missing **", output.getvalue())

    def test_update_valid_instance(self):
        """Test successful update of an instance's attribute."""
        obj = BaseModel()
        obj.save()
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd(f'update BaseModel {obj.id} name test_name')
            self.assertEqual(obj.name, "test_name")

    def test_classname_all(self):
        """Test the class-specific all command."""
        obj = BaseModel()
        obj.save()
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('BaseModel.all()')
            self.assertIn(f"[BaseModel] ({obj.id})", output.getvalue())

    def test_classname_count(self):
        """Test the class-specific count command."""
        obj1 = BaseModel()
        obj2 = BaseModel()
        obj1.save()
        obj2.save()
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd('BaseModel.count()')
            self.assertIn("2", output.getvalue())

    def test_classname_show(self):
        """Test the class-specific show command."""
        obj = BaseModel()
        obj.save()
        with patch('sys.stdout', new=StringIO()) as output:
            self.cmd.onecmd(f'BaseModel.show("{obj.id}")')
            self.assertIn(f"[BaseModel] ({obj.id})", output.getvalue())
