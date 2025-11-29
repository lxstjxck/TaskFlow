import unittest, sqlite3
from main import init_db, add_task, DB_PATH

class TestIntegration(unittest.TestCase):
    def setUp(self):
        init_db()

    def test_task_insert(self):
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("INSERT INTO tasks (title) VALUES ('Test Task')")
            conn.commit()
            res = conn.execute("SELECT * FROM tasks WHERE title='Test Task'").fetchone()
        self.assertIsNotNone(res)
