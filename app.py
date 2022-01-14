
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

line_bot_api = LineBotApi('GjDx/h+uio27gbLf+SD5nWTa+FJAbXJFQps4Omj7ldvvw3gswqUTXapZ+oWd10P0JjbfU0w55YRsQzKGxMRh9j487nYGOs1V819U6OLEzVugAu5BSUweBCKxu0M7ayXRbbX6PGMbbGZWyxwAqACgQAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('80d112842f6924a76d371c515adfeb32')

@app.route('/')
def hello():
    return "Hello Flask-Heroku"

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