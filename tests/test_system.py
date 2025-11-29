import unittest
from main import main_app, init_db

class TestSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        main_app.config["TESTING"] = True
        cls.client = main_app.test_client()

    def test_index_page(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"TaskFlow", res.data)

    def test_add_edit_delete_flow(self):
        """Добавление, редактирование, удаление"""
        # Добавить
        self.client.post("/add", data={"title": "SystemTask"}, follow_redirects=True)
        res = self.client.get("/")
        self.assertIn(b"SystemTask", res.data)

        # Редактировать
        self.client.post("/edit/1", data={"title": "Edited"}, follow_redirects=True)
        res = self.client.get("/")
        self.assertIn(b"Edited", res.data)

        # Отметить как выполненную
        self.client.get("/done/1", follow_redirects=True)
        res = self.client.get("/")
        self.assertIn(b"<s>Edited</s>".encode(), res.data)

        # Удалить
        self.client.get("/delete/1", follow_redirects=True)
        res = self.client.get("/")
        self.assertNotIn(b"Edited", res.data)

    def test_search_and_sort(self):
        """Проверка поиска и сортировки"""
        self.client.post("/add", data={"title": "Alpha"}, follow_redirects=True)
        self.client.post("/add", data={"title": "Beta"}, follow_redirects=True)
        res = self.client.get("/?order_by=title")
        self.assertEqual(res.status_code, 200)
        res = self.client.get("/?search=Alpha")
        self.assertIn(b"Alpha", res.data)
