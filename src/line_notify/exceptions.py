from requests import ConnectionError, ConnectTimeout, HTTPError, ReadTimeout


class LineNotifyHTTPError(HTTPError):
    pass


class LineNotifyConnectionTimeout(ConnectionError):
    pass


class LineNotifyConnectTimeout(ConnectTimeout):
    pass


class LineNotifyReadTimeout(ReadTimeout):
    pass
