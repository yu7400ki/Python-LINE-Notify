import platform
import unittest

from setting import TOKEN

from line_notify import LineNotify, NotifyResponse, StatusResponse


class TestLineNotify(unittest.TestCase):
    def test_notify(self) -> None:
        token = TOKEN
        message = platform.python_version()
        notification_disabled = True
        line_notify = LineNotify(token)
        response = line_notify.notify(message, notification_disabled=notification_disabled)
        self.assertIsInstance(response, NotifyResponse)
        self.assertEqual(response.status, 200)

    def test_notify_with_image(self) -> None:
        token = TOKEN
        message = platform.python_version()
        image_path = "tests/test.png"
        line_notify = LineNotify(token)
        response = line_notify.notify(message, image_path=image_path)
        self.assertIsInstance(response, NotifyResponse)
        self.assertEqual(response.status, 200)

    def test_notify_with_image_url(self) -> None:
        token = TOKEN
        message = platform.python_version()
        image_thumbnail = "https://placehold.jp/240x240.png"
        image_fullsize = "https://placehold.jp/2048x2048.png"
        line_notify = LineNotify(token)
        response = line_notify.notify(message, image_thumbnail=image_thumbnail, image_fullsize=image_fullsize)
        self.assertIsInstance(response, NotifyResponse)
        self.assertEqual(response.status, 200)

    def test_notify_with_sticker(self) -> None:
        token = TOKEN
        message = platform.python_version()
        sticker_package_id = 789
        sticker_id = 10859
        line_notify = LineNotify(token)
        response = line_notify.notify(
            message,
            sticker_package_id=sticker_package_id,
            sticker_id=sticker_id,
        )
        self.assertIsInstance(response, NotifyResponse)
        self.assertEqual(response.status, 200)

    def test_status(self) -> None:
        token = TOKEN
        line_notify = LineNotify(token)
        response = line_notify.status()
        self.assertIsInstance(response, StatusResponse)
        self.assertEqual(response.status, 200)


if __name__ == "__main__":
    unittest.main()
