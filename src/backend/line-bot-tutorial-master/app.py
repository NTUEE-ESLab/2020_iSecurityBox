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

########################################
#              Read Env                #
########################################
import os
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
SECRET       = os.getenv("SECRET")
USER_ID      = os.getenv("USER_ID")
MONGO_URL    = os.getenv("MONGO_URL")

IP           = os.getenv("IP")
PORT         = os.getenv("PORT")

# ACCESS_TOKEN = "+FE6Icc6rpurOtuIeoIfPs09NN4edeCwPNz6k2wctV9081L+X1nrCnpSZ2Pqa0ivjeKef5CMpBcA2IBPbwigw7vEN0PXRgXxhMfqcoc9eilYsfu4yNG6pg043YXeW+sLgYvwJP6DHwlVSNSBEZauSgdB04t89/1O/w1cDnyilFU="
# SECRET = "653a48c0c4c4d4498e7ae19ac024b1a9"
# USER_ID = "Ua131a4b1e537418a7a3db94d5b08b2b3"

########################################
#           Linebot Handler            #
########################################
app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(ACCESS_TOKEN)
# Channel Secret
handler = WebhookHandler(SECRET)

line_bot_api.push_message(USER_ID, 
    TextSendMessage(text="Welcome to our project!"))

########################################
#              MONGODB                 #
########################################
from mongo_server import *
mongo_col = connect_mongodb(MONGO_URL)

line_bot_api.push_message(USER_ID, 
    TextSendMessage(text="Connected to MongoDB."))

########################################
#               SOCKET                 #
########################################
# import asyncio
# import websockets

# async def echo(websocket, path):
#     line_bot_api.push_message(USER_ID, 
#         TextSendMessage(text="echo"))
#     async for message in websocket:
#         print(message,'received from client')
#         greeting = f"Hello {message}!"
#         await websocket.send(greeting)
#         print(f"> {greeting}")

#         asyncio.get_event_loop().stop()

# asyncio.get_event_loop().run_until_complete(
#     websockets.serve(echo, '0.0.0.0', 8765))
# asyncio.get_event_loop().run_forever()

# line_bot_api.push_message(USER_ID, 
#     TextSendMessage(text="Done loop"))

########################################
#               SOCKET                 #
########################################

# # 監聽所有來自 /callback 的 Post Request
# @app.route("/callback", methods=['POST'])
# def callback():
#     # get X-Line-Signature header value
#     signature = request.headers['X-Line-Signature']
#     # get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)
#     # handle webhook body
#     try:
#         handler.handle(body, signature)
#     except InvalidSignatureError:
#         abort(400)
#     return 'OK'

# # 處理訊息
# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     mongo_col = connect_mongodb(MONGO_URL)
#     message = TextSendMessage(text=event.message.text)
#     # result = query_card(MONGO_URL, card_id=message)
    
#     line_bot_api.reply_message(event.reply_token, message)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

    
