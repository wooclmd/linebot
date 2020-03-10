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

line_bot_api = LineBotApi('3uKzqxBWnx1xGkaj8p79uvNFwv1+8VIw092wiBBHxR1H+bTKkJdkKCdgPi/iJFdzArITH26PvvYqHjoe65JXJv35TfULaWcGyq7mTksYGmrsBInatc3rybVFVscX8guG01HY99LtUPfRH+SbEwzg3AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9bc788b606a9fccf208bfe6308117625')


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