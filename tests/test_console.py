#!/usr/bin/python3
"""A unittest module for the command interpreter
"""

import MySQLdb
import os
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage
from models.user import User


class TestHBNBCommand(unittest.TestCase):
    """Defines the test cases for the HBNBCommand class.
    """

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_do_create_fs(self):
        """Tests the create command with the file storage
        """

        with patch('sys.stdout', new=StringIO()) as buff:
            cons = HBNBCommand()
            cons.onecmd('create City name="Texas"')
            model_id = buff.getvalue().strip()
            buff.seek(0)
            buff.truncate()
            self.assertIn('City.{}'.format(model_id), storage.all().keys())
            cons.onecmd('show City {}'.format(model_id))
            self.assertIn("'name': 'Texas'", buff.getvalue.strip())
            buff.seek(0)
            buff.truncate()
            cons.onecmd('create User name="James" age=17 height=5.9')
            model_id2 = buff.getvalue.strip()
            self.assertIn('User.{}'.format(model_id2), storage.all().keys())
            buff.seek(0)
            buff.truncate()
            cons.onecmd('show User {}'.format(model_id2))
            self.assertIn("'name': 'James'", buff.getvalue().strip())
            self.assertIn("'age': 17", buff.getvalue().strip())
            self.assertIn("'height': 5.9", buff.getvalue().strip())
