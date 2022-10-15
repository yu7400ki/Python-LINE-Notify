import platform
import unittest

from setting import TOKEN

from line_notify import LineNotify, LineNotifyConnectTimeout, LineNotifyReadTimeout, NotifyResponse


class TestLineNotify(unittest.TestCase):
    def test_notify(self) -> None:
        token = TOKEN
        message = platform.python_version()
        notification_disabled = True
        line_notify = LineNotify(token)
        response = line_notify.notify(message, notification_disabled=notification_disabled)
        self.assertIsInstance(response, NotifyResponse)
        self.assertIsInstance(response.body, NotifyResponse.NotifyResponseBody)
        self.assertEqual(response.body.status, 200)
        self.assertEqual(response.body.message, "ok")

    def test_notify_fail(self) -> None:
        token = "invalid_token"
        message = "invalid token"
        line_notify = LineNotify(token)
        response = line_notify.notify(message)
        self.assertIsInstance(response, NotifyResponse)
        self.assertIsInstance(response.body, NotifyResponse.NotifyResponseBody)
        self.assertEqual(response.body.status, 401)
        self.assertEqual(response.body.message, "Invalid access token")

    def test_notify_timeout(self) -> None:
        token = TOKEN
        message = "timeout"
        line_notify = LineNotify(token)
        try:
            line_notify.notify(message, timeout=0.01)
        except LineNotifyConnectTimeout as e:
            print(e)
        except LineNotifyReadTimeout as e:
            print(e)

    def test_notify_with_image(self) -> None:
        token = TOKEN
        message = "with image"
        image_path = "tests/test.png"
        line_notify = LineNotify(token)
        response = line_notify.notify(message, image_path=image_path)
        self.assertIsInstance(response, NotifyResponse)
        self.assertIsInstance(response.body, NotifyResponse.NotifyResponseBody)
        self.assertEqual(response.body.status, 200)
        self.assertEqual(response.body.message, "ok")

    def test_notify_with_image_url(self) -> None:
        token = TOKEN
        message = "with image url"
        image_thumbnail = "https://placehold.jp/240x240.png"
        image_fullsize = "https://placehold.jp/2048x2048.png"
        line_notify = LineNotify(token)
        response = line_notify.notify(message, image_thumbnail=image_thumbnail, image_fullsize=image_fullsize)
        self.assertIsInstance(response, NotifyResponse)
        self.assertIsInstance(response.body, NotifyResponse.NotifyResponseBody)
        self.assertEqual(response.body.status, 200)
        self.assertEqual(response.body.message, "ok")

    def test_notify_with_sticker(self) -> None:
        token = TOKEN
        message = "with sticker"
        sticker_package_id = 789
        sticker_id = 10859
        line_notify = LineNotify(token)
        response = line_notify.notify(
            message,
            sticker_package_id=sticker_package_id,
            sticker_id=sticker_id,
        )
        self.assertIsInstance(response, NotifyResponse)
        self.assertIsInstance(response.body, NotifyResponse.NotifyResponseBody)
        self.assertEqual(response.body.status, 200)
        self.assertEqual(response.body.message, "ok")


if __name__ == "__main__":
    unittest.main()
