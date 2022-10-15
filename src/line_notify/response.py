from dataclasses import dataclass
from typing import Optional

from requests import Response

from .exceptions import LineNotifyHTTPError


class NotifyResponse(Response):
    def __init__(self) -> None:
        super().__init__()

    def raise_for_status(self) -> None:
        http_error_msg = ""

        if 400 <= self.status_code < 500:
            http_error_msg = f"{self.status_code} Client Error: {self.body.message} for url: {self.url}"

        elif 500 <= self.status_code < 600:
            http_error_msg = f"{self.status_code} Server Error: {self.body.message} for url: {self.url}"

        if http_error_msg:
            raise LineNotifyHTTPError(http_error_msg, response=self)

    @dataclass
    class NotifyResponseBody:
        status: int
        message: str

    @property
    def body(self) -> NotifyResponseBody:
        return self.NotifyResponseBody(**self.json())


class StatusResponse(Response):
    def __init__(self) -> None:
        super().__init__()

    def raise_for_status(self) -> None:
        http_error_msg = ""

        if 400 <= self.status_code < 500:
            http_error_msg = f"{self.status_code} Client Error: {self.body.message} for url: {self.url}"

        elif 500 <= self.status_code < 600:
            http_error_msg = f"{self.status_code} Server Error: {self.body.message} for url: {self.url}"

        if http_error_msg:
            raise LineNotifyHTTPError(http_error_msg, response=self)

    @dataclass
    class StatusResponseBody:
        status: int
        message: str
        target_type: Optional[str] = None
        target: Optional[str] = None

    @property
    def body(self) -> StatusResponseBody:
        body = self.json()
        return self.StatusResponseBody(
            status=body["status"],
            message=body["message"],
            target_type=body.get("targetType"),
            target=body.get("target"),
        )
