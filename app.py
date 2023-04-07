from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('eSgr/ZfwQ97a6xCToECF0rnaNWoOnrd5ZKXAHPy45IbfH4MVaid79Y1ijcm+xOzyJoMWs6Wh/IgxOXifGnMZVQg4ByC209QY3DgpUM4j7w5etOKopBpWinyE8JitpzQgq2XBcIDe0KDWXINcIgGtPgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b61daa8f353b16416ba47a90608b8ba6')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()