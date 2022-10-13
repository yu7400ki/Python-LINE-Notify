from dataclasses import dataclass
from io import BufferedReader

import requests

API_ROOT = "https://notify-api.line.me/api"


@dataclass
class NotifyResponse:
    status: int
    message: str


@dataclass
class StatusResponse:
    status: int
    message: str
    target_type: str
    target: str


@dataclass
class LineNotify:
    token: str

    def notify(
        self,
        message: str,
        image_thumbnail: str = None,
        image_fullsize: str = None,
        image_file: BufferedReader = None,
        sticker_package_id: int = None,
        sticker_id: int = None,
        notification_disabled: bool = None,
    ) -> NotifyResponse:
        path = "/notify"

        payload = {"message": message}
        if image_thumbnail is not None:
            payload["imageThumbnail"] = image_thumbnail
        if image_fullsize is not None:
            payload["imageFullsize"] = image_fullsize
        if sticker_package_id is not None:
            payload["stickerPackageId"] = str(sticker_package_id)
        if sticker_id is not None:
            payload["stickerId"] = str(sticker_id)
        if notification_disabled is not None:
            payload["notificationDisabled"] = "true" if notification_disabled else "false"

        if image_file is not None:
            files = {"imageFile": image_file}
        else:
            files = None

        header = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(API_ROOT + path, headers=header, data=payload, files=files)

        return NotifyResponse(**response.json())

    def status(self) -> StatusResponse:
        path = "/status"

        header = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(API_ROOT + path, headers=header)

        body = response.json()

        return StatusResponse(
            status=body["status"], message=body["message"], target_type=body["targetType"], target=body["target"]
        )
