# LINE Notify

## 概要

PythonのLINE Notify APIのラッパーです。

## インストール方法

Python >=3.7, <4

```
$ pip install git+https://github.com/yu7400ki/Python-LINE-Notify.git@v0.2.2
```

## 使い方

始めに以下のサイトでトークンを生成してください。

[LINE notify](https://notify-bot.line.me/ja/)

Example:

```Python
from line_notify import LineNotify

client = LineNotify("Your Token")

response = client.status()  # response is subclass for requests.Response
response.raise_for_status() # if token is valid, return None

response = client.notify("only text")
response = client.notify("with image(path)", image_path="/image.png")
response = client.notify("with image(url)", image_thumbnail=https://..., image_fullsize=https://...)
response = client.notify("with sticker", sticker_package_id=789, sticker_id=10859)
response = client.notify("If you do not wish to be notified", notification_disabled=True)

assert response.body.status == 200
assert response.body.message == "ok"
```

詳しいAPIの仕様については以下をご覧ください。

[LINE notify doc](https://notify-bot.line.me/doc/)

## License

MIT
