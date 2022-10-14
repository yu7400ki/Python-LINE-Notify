import unittest

from setting import TOKEN

from line_notify import LineNotify, StatusResponse


class TestLineNotify(unittest.TestCase):
    def test_status(self) -> None:
        token = TOKEN
        line_notify = LineNotify(token)
        response = line_notify.status()
        self.assertIsInstance(response, StatusResponse)
        self.assertEqual(response.status, 200)


if __name__ == "__main__":
    unittest.main()
