#!/usr/bin/python3
"""Module console

This module contains the HBNBCommand class, which provides
a command-line interface for managing objects in the application.
"""

import cmd
import importlib
import json
import re
from typing import Optional, Tuple, Union, Dict

from models import storage


class HBNBCommand(cmd.Cmd):
    """AirBnB clone console"""

    prompt = "(hbnb) "

    def do_quit(self, line: str) -> bool:
        """Quit command to exit the program."""
        return True

    def do_EOF(self, line: str) -> bool:
        """Exit the console using Ctrl + D."""
        print()
        return True

    def emptyline(self) -> None:
        """Override default behavior to do nothing on an empty line."""
        pass

    def do_create(self, line: str) -> None:
        """Create a new object of a given class."""
        obj_cls = self.get_class_from_input(line)
        if obj_cls is not None:
            new_obj = obj_cls()
            new_obj.save()
            print(new_obj.id)

    def do_show(self, line: str) -> None:
        """Show an object by class name and ID."""
        key = self.get_obj_key_from_input(line)
        if key is None:
            return

        saved_obj = storage.all().get(key, None)
        if saved_obj is None:
            print("** no instance found **")
        else:
            print(saved_obj)

    def do_destroy(self, line: str) -> None:
        """Delete an object by class name and ID."""
        key = self.get_obj_key_from_input(line)
        if key is None:
            return

        saved_obj = storage.all().pop(key, None)
        if saved_obj is None:
            print("** no instance found **")
        else:
            storage.save()

    def do_all(self, line: str) -> None:
        """Show all objects, optionally filtered by class name."""
        if len(line.strip()) == 0:
            result = storage.all().values()
        else:
            obj_cls = self.get_class_from_input(line)
            if obj_cls is None:
                return
            result = [item for item in storage.all().values() if isinstance(item, obj_cls)]

        print([str(item) for item in result])

    def do_update(self, line: str) -> None:
        """Update an object's attribute."""
        key = self.get_obj_key_from_input(line)
        if key is None:
            return

        saved_obj = storage.all().get(key, None)
        if saved_obj is None:
            print("** no instance found **")
        else:
            attr_name, attr_val = self.get_attribute_name_value_pair(line)
            if attr_name is None or attr_val is None:
                return

            if hasattr(saved_obj, attr_name):
                attr_type = type(getattr(saved_obj, attr_name))
                attr_val = attr_type(attr_val)
            setattr(saved_obj, attr_name, attr_val)
            saved_obj.save()

    def do_count(self, line: str) -> None:
        """Count all objects of a given class."""
        obj_cls = self.get_class_from_input(line)
        if obj_cls is None:
            return
        result = [item for item in storage.all().values() if isinstance(item, obj_cls)]

        print(len(result))

    def get_obj_key_from_input(self, line: str) -> Optional[str]:
        """Parse and return the object key from input."""
        obj_cls = self.get_class_from_input(line)
        if obj_cls is None:
            return None
        obj_id = self.get_id_from_input(line)
        if obj_id is None:
            return None
        return f"{obj_cls.__name__}.{obj_id}"

    def get_class_from_input(self, line: str) -> Optional[type]:
        """Parse and return the class from input."""
        if not line.strip():
            print("** class name missing **")
            return None
        return self.get_class(line.split()[0])

    def get_id_from_input(self, line: str) -> Optional[str]:
        """Parse and return the ID from input."""
        cmds = line.split()
        if len(cmds) < 2:
            print("** instance id missing **")
            return None
        return cmds[1]

    def get_attribute_name_value_pair(self, line: str) -> Tuple[Optional[str], Optional[str]]:
        """Parse and return a tuple of attribute name and value."""
        cmds = line.split()
        if len(cmds) < 3:
            print("** attribute name missing **")
            return None, None
        if len(cmds) < 4:
            print("** value missing **")
            return cmds[2], None
        return cmds[2], cmds[3]

    def get_class(self, name: str) -> Optional[type]:
        """Retrieve a class from the models module by name."""
        try:
            sub_module = re.sub(r'(?!^)([A-Z]+)', r'_\1', name).lower()
            module = importlib.import_module(f"models.{sub_module}")
            return getattr(module, name)
        except (ImportError, AttributeError):
            print("** class doesn't exist **")
            return None

    def default(self, line: str) -> None:
        """Handle commands in the form `ClassName.command(args)`."""
        cls_name, func_name, obj_id, args = self.parse_input(line)

        if cls_name is None:
            print("** class name missing **")
            return

        if func_name == "count":
            self.do_count(cls_name)
        elif func_name == "all":
            self.do_all(cls_name)
        elif func_name == "show":
            self.do_show(f"{cls_name} {obj_id}")
        elif func_name == "destroy":
            self.do_destroy(f"{cls_name} {obj_id}")
        elif func_name == "update":
            if isinstance(args, str):
                self.do_update(f"{cls_name} {obj_id} {args}")
            elif isinstance(args, dict):
                for k, v in args.items():
                    self.do_update(f"{cls_name} {obj_id} {k} {v}")

    def parse_input(self, input: str) -> Tuple[Optional[str], Optional[str], Optional[str], Union[str, Dict]]:
        """Parse complex input in the form `ClassName.command(args)`."""
        args = input.split('.')
        if len(args) != 2:
            return None, None, None, None

        cls_name = args[0]
        func_w_args = args[1].split("(")
        if len(func_w_args) != 2:
            return cls_name, None, None, None

        func_name = func_w_args[0]
        f_args = func_w_args[1].strip(')')

        id_match = re.match(r'(^"[\w-]+")', f_args)
        obj_id = id_match.group().strip('"') if id_match else None

        dict_match = re.match(r'(\{.*\})', f_args)
        if dict_match:
            return cls_name, func_name, obj_id, json.loads(dict_match.group())

        return cls_name, func_name, obj_id, f_args.strip(",")

if __name__ == '__main__':
    HBNBCommand().cmdloop()

