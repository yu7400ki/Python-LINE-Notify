"""
A wrapper for LINE Notify API
"""

import os.path
from dataclasses import dataclass
from typing import Dict, Optional, Tuple, Union

import requests

from .exceptions import LineNotifyConnectTimeout, LineNotifyReadTimeout
from .response import NotifyResponse, StatusResponse

API_ROOT = "https://notify-api.line.me/api"

_Timeout = Optional[Union[float, Tuple[float, float], Tuple[float, None]]]


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

        payload: Dict[str, Union[str, int, bool]] = {"message": message}
        if image_thumbnail is not None:
            payload["imageThumbnail"] = image_thumbnail
        if image_fullsize is not None:
            payload["imageFullsize"] = image_fullsize
        if sticker_package_id is not None:
            payload["stickerPackageId"] = sticker_package_id
        if sticker_id is not None:
            payload["stickerId"] = sticker_id
        if notification_disabled is not None:
            payload["notificationDisabled"] = notification_disabled

        if image_path is not None and os.path.isfile(image_path):
            f = open(image_path, "rb")
            files = {"imageFile": f}
        else:
            files = None

        header = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.post(API_ROOT + path, headers=header, data=payload, files=files, timeout=timeout)
        except requests.exceptions.ConnectTimeout as e:
            raise LineNotifyConnectTimeout(e)
        except requests.exceptions.ReadTimeout as e:
            raise LineNotifyReadTimeout(e)

        if files is not None:
            f.close()

        return NotifyResponse(response)

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

        try:
            response = requests.get(API_ROOT + path, headers=header, timeout=timeout)
        except requests.exceptions.ConnectTimeout as e:
            raise LineNotifyConnectTimeout(e)
        except requests.exceptions.ReadTimeout as e:
            raise LineNotifyReadTimeout(e)

        return StatusResponse(response)
