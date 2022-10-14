from requests import ConnectTimeout, HTTPError, ReadTimeout


class LineNotifyHTTPError(HTTPError):
    pass


class LineNotifyConnectTimeout(ConnectTimeout):
    pass


class LineNotifyReadTimeout(ReadTimeout):
    pass
