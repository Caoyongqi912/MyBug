import unittest
import random
from faker import Faker
from APP import create_app

app = create_app()


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        app.testing = True
        self.f = Faker()

        self.body = {
            "productId": random.randint(1, 10),
            "projectId": random.randint(1, 10),
            "platformId": random.randint(1, 10),
            "buildId": random.randint(1,10),
            "title": self.f.sentence(),
            "name": self.f.name(),
            "password": self.f.password(),
            "level": random.choice(["p1", "p2", "p3", "p4"]),
            "assignedTo": random.randint(1, 10),
            "mailTo": random.randint(1, 10),
            "stepBody": self.f.text()
        }
        self.client = app.test_client()

    def test_01(self):
        resp = app.test_client().post("/api/bugOpt", json=self.body).json

        print(resp)
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
