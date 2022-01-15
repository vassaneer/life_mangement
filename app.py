
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

from dotenv import load_dotenv
import os
from os.path import join, dirname
from notion import notion

app = Flask(__name__)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
line_bot_api = LineBotApi(os.environ.get("LINEBOT"))
handler = WebhookHandler(os.environ.get("SECRET"))
notionSecret = os.environ.get("NOTIONSECRET")
notionDB = os.environ.get("NOTIONDB")

notion = notion(notionSecret, notionDB)
notion.taskToday()

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
    res = ""
    if event.message.text == "task":
        res = notion.taskToday()

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=res))


if __name__ == "__main__":
    app.run()