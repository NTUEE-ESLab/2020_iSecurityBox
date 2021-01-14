########################################
#              Read Env                #
########################################
import os
import json
from enum import Enum
from dotenv import load_dotenv

load_dotenv()
LINE_TOKEN  = os.getenv("LINE_TOKEN")
LINE_SECRET = os.getenv("LINE_SECRET")
USER_ID     = os.getenv("USER_ID")
MONGO_URL   = os.getenv("MONGO_URL")
SERVER_IP   = os.getenv("SERVER_IP")

class LineMode(Enum):
    DISABLED = 'disabled'
    REGISTER = 'register'

LINE_MODE = LineMode.DISABLED
CARD_ID   = ""

########################################
#           Linebot Import             #
########################################
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('LEOMPi6ttMe5cyz6+pGTmEYKcFPvvqFAsIgS+XAUHd43lZlxxlnFwrCBfmxgMiFEd7bhNax3DIJE4UYK4z7xXcxos/HtKUiedVGKQkFKJInuhRWgbDQ4XrlnXcFVvNJIqfZdG/rOm2czJv4blLihgAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('759cfee2a2b69169e62d5471a1164ed0')

# line_bot_api.push_message("U87718332e072f8e73f876e9d5c76c42c", TextSendMessage(text="hello"))

########################################
#              MONGODB                 #
########################################
from functions.mongo_server import *
mongo_col = connect_mongodb(MONGO_URL)

line_bot_api.push_message(USER_ID, 
    TextSendMessage(text="> Connected to MongoDB from reply server."))

########################################
#               Linebot                #
########################################
# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global LINE_MODE
    global CARD_ID

    line_message = ""
    user_action = ""
    
    # register case
    if LINE_MODE == LineMode.REGISTER:
        # user reply is the user name
        if not CARD_ID:
            line_bot_api.reply_message(event.reply_token, 
                TextSendMessage(text="No card provided. Break."))
        else:
            results = register_card(MONGO_URL, CARD_ID, event.message.text)
            line_bot_api.reply_message(event.reply_token, 
                TextSendMessage(text=f"Status: {results['status']}. Message: {results['message']}."))
        
        CARD_ID   = ""
        LINE_MODE = LineMode.DISABLED
        return

    # disabled case
    try:
        user_reply = json.loads(event.message.text)
    except:
        line_bot_api.reply_message(event.reply_token, 
            TextSendMessage(text="Do nothing."))
        LINE_MODE = LineMode.DISABLED
        return

    if isinstance(user_reply, dict) and \
        'card' in user_reply and 'action' in user_reply:
        user_action = user_reply['action']
        CARD_ID     = user_reply['card']
    
        if user_action == 'register':
            line_bot_api.reply_message(event.reply_token, 
                TextSendMessage(text="Please enter the user name:"))
            LINE_MODE = LineMode.REGISTER
        else:
            line_bot_api.reply_message(event.reply_token, 
                TextSendMessage(text="Unknown person is blocked."))
            LINE_MODE = LineMode.DISABLED
    else:
        line_bot_api.reply_message(event.reply_token, 
            TextSendMessage(text="Do nothing."))
        LINE_MODE = LineMode.DISABLED

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
