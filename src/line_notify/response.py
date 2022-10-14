from dataclasses import dataclass
from typing import Optional

import requests


class _BaseResponse:
    def __init__(self, response: requests.Response) -> None:
        self.response = response
        self.headers = response.headers

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.response!r})"

    def raise_for_status(self) -> None:
        self.response.raise_for_status()

    @property
    def status(self) -> int:
        return self.response.status_code

    @property
    def ok(self) -> bool:
        return self.response.ok


class NotifyResponse(_BaseResponse):
    def __init__(self, response: requests.Response) -> None:
        super().__init__(response)

    @dataclass
    class NotifyResponseBody:
        status: int
        message: str

    @property
    def body(self) -> NotifyResponseBody:
        return self.NotifyResponseBody(**self.response.json())


class StatusResponse(_BaseResponse):
    def __init__(self, response: requests.Response) -> None:
        super().__init__(response)

    @dataclass
    class StatusResponseBody:
        status: int
        message: str
        target_type: Optional[str] = None
        target: Optional[str] = None

    @property
    def body(self) -> StatusResponseBody:
        body = self.response.json()
        return self.StatusResponseBody(
            status=body["status"],
            message=body["message"],
            target_type=body.get("targetType"),
            target=body.get("target"),
        )
