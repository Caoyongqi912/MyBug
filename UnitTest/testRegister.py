import unittest
from faker import Faker
from APP import create_app

app = create_app()


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        app.testing = True
        self.f = Faker()

        self.body = {
            "account": self.f.name(),
            "name": self.f.name(),
            "password": self.f.password(),
            "admin": True,
            "gender": False
        }
        self.client = app.test_client()

    def test_register01(self):
        self.body.pop("account")
        resp = app.test_client().post("/api/register", json=self.body).json
        self.assertEqual(resp['code'], 1)

    def test_register02(self):
        self.body['account'] = ""
        resp = app.test_client().post("/api/register", json=self.body).json
        self.assertEqual(resp['code'], 1)

    def test_register03(self):
        self.body['name'] = None
        resp = app.test_client().post("/api/register", json=self.body).json
        self.assertEqual(resp['code'], 1)

    def test_register04(self):
        self.body['name'] = ""
        resp = app.test_client().post("/api/register", json=self.body).json
        self.assertEqual(resp['code'], 1)

    def test_register05(self):
        self.body.pop("name")
        resp = app.test_client().post("/api/register", json=self.body).json
        self.assertEqual(resp['code'], 1)

    def test_register06(self):
        app.test_client().post("/api/register", json=self.body)
        resp = app.test_client().post("/api/register", json=self.body).json
        self.assertEqual(resp['code'], 1)

    def test_register07(self):
        self.body.pop("password")
        resp = app.test_client().post("/api/register", json=self.body).json
        self.assertEqual(resp['code'], 1)

    def test_register08(self):
        self.body["password"] = ""
        resp = app.test_client().post("/api/register", json=self.body).json
        self.assertEqual(resp['code'], 1)

    def test_register09(self):
        self.body["admin"] = 1123
        resp = app.test_client().post("/api/register", json=self.body).json
        self.assertEqual(resp['code'], 22)

    def test_register10(self):
        self.body["gender"] = 1123
        resp = app.test_client().post("/api/register", json=self.body).json
        self.assertEqual(resp['code'], 22)


if __name__ == '__main__':
    unittest.main()
