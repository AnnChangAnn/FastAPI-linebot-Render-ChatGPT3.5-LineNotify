# -*- coding: utf-8 -*-
#import logging, uvicorn
from datetime import datetime
import os
from openai import OpenAI
import json
from fastapi import FastAPI, Request, HTTPException

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

from Notify import weather_notify, announce_notify, star_sign_notify

# get env variables
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN',  None))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET',  None))

# openai.api_key = os.getenv('OPENAI_APIKEY', None)
client = OpenAI(
  api_key=os.getenv('OPENAI_APIKEY', None),  # this is also the default, it can be omitted
)

openai_model = os.getenv("OPENAI_MODEL", None)
openai_temperature = float(os.getenv("OPENAI_TEMPERATURE", None))
openai_max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", None))
weather_token = os.getenv('WEATHER_TOKEN', None)
introduce_msg = os.getenv('INTRODUCE_MESSAGE', None)
announce_token = os.getenv('ANNOUNCE_TOKEN', None)

star_sign_dict = {
    '牡羊座': '0', '金牛座': '1', '雙子座': '2', '巨蟹座': '3',
    '獅子座': '4', '處女座': '5', '天秤座': '6', '天蠍座': '7',
    '射手座': '8', '摩羯座': '9', '水瓶座': '10', '雙魚座': '11',
    '双子座': '2', '天平座': '6', '天枰座': '6', '魔羯座': '9',
    '水平座': '10', '双魚座': '11', '水平': '10', '双魚': '11',
    '牡羊': '0', '金牛': '1', '雙子': '2', '巨蟹': '3',
    '獅子': '4', '處女': '5', '天秤': '6', '天蠍': '7',
    '射手': '8', '摩羯': '9', '水瓶': '10', '雙魚': '11',
    '双子': '2', '天平': '6', '天枰': '6', '魔羯': '9'
}

class ChatGPT:  
    def __init__(self):
        self.model = openai_model
        self.temperature = openai_temperature
        self.max_tokens = openai_max_tokens

    def get_response(self, message):
        prompt = message[4:]
        response = client.chat.completions.create(
	            model = self.model,
                messages = [
                    {'role': 'user', 'content': prompt}
                ],
                temperature = self.temperature,
                max_tokens = self.max_tokens
                )
        reply_msg = response.choices[0].message.content.strip()
        print('AI回答內容' + reply_msg)
        return reply_msg


chatgpt = ChatGPT()
app = FastAPI()


def check_group_or_user(eventsource):
    if hasattr(eventsource, "group_id"):
        return eventsource.group_id
    else:
        return eventsource.user_id

# test method
@app.get("/test") # 指定 api 路徑 (get方法)
async def hello():
	return "Hello World for AnnChangAnn!!"

# Line Weather Notify
@app.post("/lineNotifyWeather")
async def lineNotifyWeather():
    # return  lineNotifyMessage('1',values)
    weather_notify.lineNotifyWeather(weather_token)
    return 'OK'

# Keep Alive
@app.post("/tickingclock")
async def TickingClock():
    print('TickingClock: ' + str(datetime.now()))

# 監聽所有來自 /callback 的 Post Request
@app.post("/callback")
async def callback(request: Request):
    signature = request.headers["X-Line-Signature"]
    body = await request.body()
    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Missing Parameters")
    return "OK"

# 加入群組自動發送
@handler.add(JoinEvent)
def handle_join(event):
    message = TextSendMessage(text = introduce_msg)

    line_bot_api.reply_message(event.reply_token,message)
    print("JoinEvent =", JoinEvent)

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handling_message(event):
    #replyToken = event.reply_token
    user_message = str(event.message.text)
    print(user_message)
    
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":

        #star sign response
        star_sign = user_message.replace(' ','')
        if len(star_sign) >= 4:
            star_sign = star_sign[1:4]
            print(star_sign)

        if len(star_sign) == 3 and star_sign in star_sign_dict:
            star_sign_daily = star_sign_notify.star_sign_daily(star_sign, star_sign_dict[star_sign])
            message = TextSendMessage(text = star_sign_daily)
            line_bot_api.reply_message(event.reply_token, message)


        elif user_message == "!蒜頭自介" or user_message == "！蒜頭自介":
            message = TextSendMessage(text = introduce_msg)
            line_bot_api.reply_message(event.reply_token, message)

        elif user_message.find('請問蒜頭') == 0:
            #event_id = check_group_or_user(event.source)
            reply_msg = chatgpt.get_response(user_message)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_msg))
            #line_bot_api.push_message(event_id, TextSendMessage(text=reply_msg))
        
        # announce to line group
        elif user_message.find('！公告 ') == 0 or user_message.find('!公告 ') == 0:
            announce_notify.lineNotifyAnnounce(user_message[4:], announce_token)

        # 幹話
        elif user_message == "好美":
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "哪有你美"))
        elif user_message in ["好阿", "好啊", "好"]:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = user_message))
        elif user_message == "!!測試":
            event_id = check_group_or_user(event.source)
            print(event_id)
            #time.sleep(31)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="測試成功!"))
            #line_bot_api.push_message(event_id, TextSendMessage(text="測試成功!"))

