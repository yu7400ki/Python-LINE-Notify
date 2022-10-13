"""
A wrapper for LINE Notify API
"""

import os.path
from dataclasses import dataclass
from typing import Optional, Tuple, Union

import requests

API_ROOT = "https://notify-api.line.me/api"

_Timeout = Optional[Union[float, Tuple[float, float], Tuple[float, None]]]


@dataclass
class NotifyResponse:
    status: int
    message: str


@dataclass
class StatusResponse:
    status: int
    message: str
    target_type: Optional[str]
    target: Optional[str]


@dataclass
class LineNotify:
    """Create a LineNotify instance
    doc: https://notify-bot.line.me/doc/

    args:
        token: LINE Notify access token
    returns:
        LineNotify instance
    """

    token: str

    def notify(
        self,
        message: str,
        image_thumbnail: str = None,
        image_fullsize: str = None,
        image_path: str = None,
        sticker_package_id: int = None,
        sticker_id: int = None,
        notification_disabled: bool = None,
        timeout: _Timeout = None,
    ) -> NotifyResponse:
        """Notify message to LINE Notify

        Args:
            message (str): Message to send
            image_thumbnail (str, optional): URL of image thumbnail. Defaults to None. Must be set with image_fullsize.
            image_fullsize (str, optional): URL of image fullsize. Defaults to None. Must be set with image_thumbnail.
            image_path (str, optional): Path of image to send. Defaults to None.
            sticker_package_id (int, optional): Package ID of sticker. Defaults to None. Must be set with sticker_id.
            sticker_id (int, optional): ID of sticker. Defaults to None. Must be set with sticker_package_id.
            notification_disabled (bool, optional): Disable notification. Defaults to None.
            timeout (Optional[Union[float, Tuple[float, float], Tuple[float, None]]], optional):
            Timeout of request. Defaults to None.

        Returns:
            NotifyResponse: Response from LINE Notify API
        """
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

        if image_path is not None and os.path.isfile(image_path):
            files = {"imageFile": open(image_path, "rb")}
        else:
            files = None

        header = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(API_ROOT + path, headers=header, data=payload, files=files, timeout=timeout)

        return NotifyResponse(**response.json())

    def status(self, timeout: _Timeout = None) -> StatusResponse:
        """Get status of LINE Notify

        args:
            timeout (Optional[Union[float, Tuple[float, float], Tuple[float, None]]], optional):
            Timeout of request. Defaults to None.

        returns:
            StatusResponse: Response from LINE Notify API
        """
        path = "/status"

        header = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(API_ROOT + path, headers=header, timeout=timeout)
        body = response.json()

        if body["status"] == 200:
            return StatusResponse(
                status=body["status"], message=body["message"], target_type=body["targetType"], target=body["target"]
            )
        else:
            return StatusResponse(status=body["status"], message=body["message"], target_type=None, target=None)
