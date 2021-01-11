import unittest
from APP import create_app
from faker import Faker

app = create_app()


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.f = Faker()
        app.testing = True
        self.client = app.test_client()
        self.username = "cyq"
        self.password = "cyq"

    def tearDown(self) -> None:
        pass

    def test_login_without_data(self):
        resp = app.test_client().post("/api/login", json={}).json
        self.assertEqual(resp['code'], 1)
        self.assertEqual(resp['data'], None)
        self.assertEqual(resp['msg'], "account 不能为空")

    def test_login_without_account(self):
        resp = app.test_client().post("/api/login", json={"account": ""}).json
        self.assertEqual(resp['code'], 1)
        self.assertEqual(resp['data'], None)
        self.assertEqual(resp['msg'], "account 不能为空")

    def test_login_without_password(self):
        resp = app.test_client().post("/api/login", json={"account": "cyq", "password": ""}).json
        self.assertEqual(resp['code'], 1)
        self.assertEqual(resp['data'], None)
        self.assertEqual(resp['msg'], "password 不能为空")

    def test_login(self):
        resp = app.test_client().post("/api/login", json={"account": "cyq", "password": "cyq"}).json
        self.assertEqual(resp['code'], 0)
        self.assertEqual(resp['msg'], "ok")

    def test_register(self):
        name = self.f.pystr()
        info = {
            "account": name,
            "name": name[5:],
            "password": name,
            "admin": False

        }
        resp = app.test_client().post("/api/register", json=info).json
        print(resp)
        self.assertEqual(resp['code'], 1)
        self.assertEqual(resp['msg'], None)
        self.assertNotEqual(resp['data'], None)

    def test_register_without_data(self):
        resp = app.test_client().post("/api/register", json={}).json
        self.assertEqual(resp['code'], 1)
        self.assertEqual(resp['data'], None)
        self.assertEqual(resp['msg'], "account 不能为空")

    def test_register_without_account(self):
        resp = app.test_client().post("/api/register", json={"account": "", "password": "123"}).json
        self.assertEqual(resp['code'], 1)
        self.assertEqual(resp['data'], None)
        self.assertEqual(resp['msg'], "account 不能为空")

    def test_register_without_name(self):
        resp = app.test_client().post("/api/register", json={"account": "cyq", "password": None}).json
        self.assertEqual(resp['code'], 1)
        self.assertEqual(resp['data'], None)
        self.assertEqual(resp['msg'], "name 不能为空")

    def test_register_without_password(self):
        resp = app.test_client().post("/api/register",
                                      json={"account": self.f.pystr(), "name": self.f.pystr(), "password": None}).json
        self.assertEqual(resp['code'], 1)
        self.assertEqual(resp['data'], None)
        self.assertEqual(resp['msg'], "password 不能为空")

    def test_register_with_err_gender(self):
        resp = app.test_client().post("/api/register",
                                      json={"account": self.f.pystr(), "name": self.f.pystr(), "password": "None",
                                            "gender": 3}).json
        print(resp)
        self.assertEqual(resp['code'], 1)
        self.assertEqual(resp['data'], None)
        self.assertEqual(resp['msg'], "admin: None is not bool")

    def test_register_with_err_departmentId(self):
        resp = app.test_client().post("/api/register",
                                      json={"account": self.f.pystr(), "name": self.f.pystr(), "password": "None",
                                            "gender": True, "departmentId": -1}).json
        print(resp)
        self.assertEqual(resp['code'], 1)
        self.assertEqual(resp['data'], None)
        self.assertEqual(resp['msg'], "admin: None is not bool")


if __name__ == '__main__':
    unittest.main()
