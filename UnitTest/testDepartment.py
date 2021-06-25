import unittest
import random
from faker import Faker
from APP import create_app



app = create_app()

class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.f = Faker()
        app.testing = True
        self.client = app.test_client()
        self.username = "cyq"
        self.password = "cyq"

    def test_create_department(self):
        resp = app.test_client().post("/api/departmentOpt", json={}).json
        print(resp)
        # self.assertEqual(resp['code'], 1)
        # self.assertEqual(resp['data'], None)
        # self.assertEqual(resp['msg'], "account 非法参数！")


    # def test_get_departmeny(self):
    #     resp = app.test_client().get("/api/departmentOpt",params={"departmentId":1})
    #     print(resp)
    #
if __name__ == '__main__':
    unittest.main()
