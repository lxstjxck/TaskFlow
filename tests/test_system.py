import unittest
from main import main_app, init_db

class TestSystem(unittest.TestCase):
    def setUp(self):
        init_db()
        main_app.config['TESTING'] = True
        self.client = main_app.test_client()

    # проверка загрузки главной страницы
    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"TaskFlow", response.data)

    # добавление задачи через пост
    def test_add_task_post(self):
        response = self.client.post("/add", data={"title": "New Task"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"NewTask", response.data)