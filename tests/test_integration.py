import unittest
import sqlite3
from main import init_db

class TestIntegration(unittest.TestCase):
    def setUp(self):
        init_db()

    # проверка добавления задачи и сохранения
    def test_insert_task(self):
        with sqlite3.connect("tasks.db") as conn:
            conn.execute("INSERT INTO tasks (title) VALUES ('Test')")
            conn.commit()
            result = conn.execute("SELECT * FROM tasks WHERE title='Test'").fetchone()
        self.assertIsNotNone(result)