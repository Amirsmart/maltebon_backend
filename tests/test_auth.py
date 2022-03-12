import sys
sys.path.insert(1, '../')
from config import init_config
from tools.db_tool import init_db

from db_models.users import add_user
import unittest



class TestApp(unittest.TestCase):
    """Unit tests defined for app.py"""

    def test_register(self):
        """Test return backwards simple string"""
        configs = init_config()
        MYSQL_HOST = configs['MYSQL_HOST']
        MYSQL_USER = configs['MYSQL_USER']
        MYSQL_PASSWORD = configs['MYSQL_PASSWORD']
        MYSQL_DB = configs['MYSQL_DB']
        engine = init_db(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB)
        name = "test_name"
        email = "test_email@mail.com"
        password = "test_password"
        self.assertEqual(True, add_user(name, email, password, engine))

if __name__ == "__main__":
    unittest.main()