import unittest
from main import main_app, init_db

class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        main_app.config["TESTING"] = True
        cls.client = main_app.test_client()

    def test_add_get_done_delete_api(self):
        """Полный цикл CRUD через API"""
        # Добавить
        res = self.client.post("/api/add", json={"title": "API Task"})
        self.assertEqual(res.status_code, 200)

        # Получить список
        res = self.client.get("/api/tasks")
        self.assertIn(b"API Task", res.data)

        # Отметить как выполненную
        res = self.client.patch("/api/done/1")
        self.assertEqual(res.status_code, 200)

        # Удалить
        res = self.client.delete("/api/delete/1")
        self.assertEqual(res.status_code, 200)

    def test_add_without_title(self):
        """Ошибка при пустом заголовке"""
        res = self.client.post("/api/add", json={})
        self.assertEqual(res.status_code, 400)
