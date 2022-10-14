import unittest

from setting import TOKEN

from line_notify import (
    LineNotify,
    LineNotifyConnectTimeout,
    LineNotifyHTTPError,
    LineNotifyReadTimeout,
    StatusResponse,
)


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
        try:
            response.raise_for_status()
        except LineNotifyHTTPError as e:
            print(e)

    def test_status_timeout(self) -> None:
        token = TOKEN
        line_notify = LineNotify(token)
        try:
            line_notify.status(timeout=0.01)
        except LineNotifyConnectTimeout as e:
            print(e)
        except LineNotifyReadTimeout as e:
            print(e)

    def test_status_encoding(self) -> None:
        token = TOKEN
        line_notify = LineNotify(token)
        response = line_notify.status()
        response.encoding = "utf-8"
        self.assertIsInstance(response, StatusResponse)
        self.assertIsInstance(response.body, StatusResponse.StatusResponseBody)
        self.assertEqual(response.body.status, 200)
        self.assertEqual(response.body.message, "ok")


if __name__ == "__main__":
    unittest.main()
