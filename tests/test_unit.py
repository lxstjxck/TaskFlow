import unittest
from main import init_db

class TestUnit(unittest.TestCase):
    # БД создается без ошибок
    def test_db_creation(self):
        try:
            init_db()
        except Exception as e:
            self.fail(f"init_db вызвал исключение: {e}")