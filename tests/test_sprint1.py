import sys
sys.path.insert(1, '../')



from flask import session

from db_models.plugins import get_one_plugin, get_one_plugin_crud, init_plugins, set_plugin_token
from config import init_config
from tools.db_tool import init_db, init_tables
from unittest.mock import patch
from unittest.mock import Mock
import tools.db_tool
from alchemy_mock.mocking import AlchemyMagicMock

import sqlalchemy as db

from db_models.users import UserModel, add_user, check_one_user, get_by_username
import unittest

session = None
engine = None

class TestApp(unittest.TestCase):
    global session
    """Unit tests defined for app.py"""

    def test4_set_plugin(self):
        plugin = get_one_plugin('whois' , -1 , engine)
        user = get_by_username('test_name3' ,engine)
        set_plugin_token(plugin , user ,engine , 'test' , 'test2' , 'test3' )
        
        
    def test3_init_plugin(self):
        init_plugins(engine)
        
    def test2_login(self):
        name = "test_name3"
        password = "test_password"
        self.assertIsNotNone(check_one_user(name , password , engine))
    def test1_register(self ):
        """Test return backwards simple string"""
        configs = init_config()
        MYSQL_HOST = configs['MYSQL_HOST']
        MYSQL_USER = configs['MYSQL_USER']
        MYSQL_PASSWORD = configs['MYSQL_PASSWORD']
        MYSQL_DB = configs['MYSQL_DB']
        #engine = init_db(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB)
        #engine = mock_sqlalchemy()
        #engine = Mock(items=[])
        name = "test_name3"
        email = "test_email3@mail.com"
        password = "test_password"
        self.assertEqual(True, add_user(name, email, password, engine ))


if __name__ == "__main__":
    engine = db.create_engine('sqlite:///:memory:')
    init_tables(engine)

    unittest.main()