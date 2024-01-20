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

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_do_create_db(self):
        """Tests the create command with a database storage
        """

        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            # Creating a model with empty attributes
            with self.assertRaises(sqlalchemy.exc.OperationalError):
                cons.onecmd('create User')
            # Creating a User instance with attributes
            cout.seek(0)
            cout.truncate()
            cons.onecmd('create User email="john@snow.com" password="johnpwd"')
            model_id3 = cout.getvalue().strip()
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD')
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(model_id3))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('john@snow.com', result)
            self.assertIn('johnpwd', result)
            cursor.close()
            dbc.close()
