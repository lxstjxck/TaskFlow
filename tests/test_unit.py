import unittest
from main import init_db, get_all_tasks

class TestUnit(unittest.TestCase):
    def test_db_init_and_fetch(self):
        init_db()
        tasks = get_all_tasks()
        self.assertIsInstance(tasks, list)
