import unittest


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        app.testing = True
        self.f = Faker()
    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
