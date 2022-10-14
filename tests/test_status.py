import unittest

from setting import TOKEN

from line_notify import LineNotify, StatusResponse


class TestLineNotify(unittest.TestCase):
    def test_status(self) -> None:
        token = TOKEN
        line_notify = LineNotify(token)
        response = line_notify.status()
        self.assertIsInstance(response, StatusResponse)
        self.assertIsInstance(response.body, StatusResponse.StatusResponseBody)
        self.assertEqual(response.body.status, 200)

    def test_status_fail(self) -> None:
        token = "invalid_token"
        line_notify = LineNotify(token)
        response = line_notify.status()
        self.assertIsInstance(response, StatusResponse)
        self.assertIsInstance(response.body, StatusResponse.StatusResponseBody)
        self.assertEqual(response.body.status, 401)


if __name__ == "__main__":
    unittest.main()
