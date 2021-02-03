import unittest
from APP import create_app
from faker import Faker
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
    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
