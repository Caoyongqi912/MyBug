import unittest
import random
from faker import Faker
from APP import create_app
from COMMENT.myRequest import MyRequest

req = MyRequest()


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.f = Faker()

        self.body = {
            "projectId": 11,
            "productId": 9,
            "platformId": random.randint(11, 15),
            "buildId": random.randint(11, 20),
            "title": self.f.sentence(),
            'assignedTo': random.randint(1, 11),
            "mailTo": random.randint(1, 11),
            "stepsBody": self.f.text(),
            "level": random.choice(['p1', 'p2', 'p3', 'p4']),
            "priority": random.choice(['p1', 'p2', 'p3', 'p4']),

        }

    def test_addSuccessBug(self):
        resp = req.go("POST", url="api/bugOpt", body=self.body)
        self.assertEqual(resp.json()['code'], 0)

    def test_addErrorBug01(self):
        self.body.pop("title")
        resp = req.go("POST", url="api/bugOpt", body=self.body)
        self.assertEqual(resp.json()['code'], 44)

    def test_addErrorBug02(self):
        self.body['platformId'] = "1"
        resp = req.go("POST", url="api/bugOpt", body=self.body)
        self.assertEqual(resp.json()['code'], 44)

    def test_addErrorBug03(self):
        self.body['level'] = 'err'
        resp = req.go("POST", url="api/bugOpt", body=self.body)
        self.assertEqual(resp.json()['code'], 44)

    def test_putSuccessBug(self):
        body = {'bugID': 1, "title": self.f.sentence()}
        resp = req.go("PUT", url="api/bugOpt", body=body)
        print(resp.json())
        self.assertEqual(resp.json()['code'], 0)

    def test_putErrorBug01(self):
        body = {'bugID': 1, "projectId": 1}
        resp = req.go("PUT", url="api/bugOpt", body=body)
        self.assertEqual(resp.json()['code'], 21)

    def test_putErrorBug02(self):
        body = {'bugID': 1, "productId": 1}
        resp = req.go("PUT", url="api/bugOpt", body=body)
        self.assertEqual(resp.json()['code'], 21)

    def test_putErrorBug03(self):
        body = {'bugID': 1, "productId": 1, "projectId": 3}
        resp = req.go("PUT", url="api/bugOpt", body=body)
        self.assertEqual(resp.json()['code'], 21)

    def test_putErrorBug04(self):
        body = {'bugID': 1, "productId": 1, "projectId": 9}
        resp = req.go("PUT", url="api/bugOpt", body=body)
        print(resp.json())
        self.assertEqual(resp.json()['code'], 21)


if __name__ == '__main__':
    unittest.main()
