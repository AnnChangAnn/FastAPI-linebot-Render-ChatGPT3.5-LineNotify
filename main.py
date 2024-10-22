# -*- coding: utf-8 -*-
#import logging, uvicorn
from datetime import datetime
import os
import json
import random
from fastapi import FastAPI, Request, HTTPException

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

from Class import chatgpt
from Notify import weather_notify, announce_notify, star_sign_notify

# get env variables
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN',  None))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET',  None))

weather_token = os.getenv('WEATHER_TOKEN', None)
star_sign_token = os.getenv('STAR_SIGN_TOKEN', None)
introduce_msg = os.getenv('INTRODUCE_MESSAGE', None)
announce_token = os.getenv('ANNOUNCE_TOKEN', None)

# init dictionary
star_sign_map = {
    '牡羊座': '牡羊座', '金牛座': '金牛座', '雙子座': '雙子座', '巨蟹座': '巨蟹座',
    '獅子座': '獅子座', '處女座': '處女座', '天秤座': '天秤座', '天蠍座': '天蠍座',
    '射手座': '射手座', '摩羯座': '摩羯座', '水瓶座': '水瓶座', '雙魚座': '雙魚座',
    '双子座': '雙子座', '天平座': '天秤座', '天枰座': '天秤座', '魔羯座': '摩羯座',
    '水平座': '水瓶座', '双魚座': '雙魚座', '水平': '水瓶座', '双魚': '雙魚座',
    '牡羊': '牡羊座', '金牛': '金牛座', '雙子': '雙子座', '巨蟹': '巨蟹座',
    '獅子': '獅子座', '處女': '處女座', '天秤': '天秤座', '天蠍': '天蠍座',
    '射手': '射手座', '摩羯': '摩羯座', '水瓶': '水瓶座', '雙魚': '雙魚座',
    '双子': '雙子座', '天平': '天秤座', '天枰': '天秤座', '魔羯': '摩羯座'
}
star_sign_dict = {
    '牡羊座': '0', '金牛座': '1', '雙子座': '2', '巨蟹座': '3',
    '獅子座': '4', '處女座': '5', '天秤座': '6', '天蠍座': '7',
    '射手座': '8', '摩羯座': '9', '水瓶座': '10', '雙魚座': '11'
}
special_chars = {"!", "！"}

# init ChatGPT
chatGPT = chatgpt.ChatGPT()
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
    weather_notify.lineNotifyWeather(weather_token)
    return 'OK'

# Line Weather Notify
@app.post("/lineNotifyStarSign")
async def lineNotifyStarSign():
    random_star_sign = random.choice(list(star_sign_dict.keys()))
    star_sign_notify.lineNotifyStarSign(star_sign_token, random_star_sign, star_sign_dict[random_star_sign])
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

    print(event)

    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":

        #star sign response
        star_sign = user_message.replace(' ','')
        star_check = False
        if len(star_sign) in {3, 4} and star_sign[0] in special_chars:
            star_sign = star_sign[1:]
            star_check = True
        
        if star_check and len(star_sign) in {2, 3} and star_sign in star_sign_map:
            star_sign = star_sign_map[star_sign]
            star_sign_daily = star_sign_notify.StarSignDaily(star_sign, star_sign_dict[star_sign])
            message = TextSendMessage(text = star_sign_daily)
            line_bot_api.reply_message(event.reply_token, message)
        
        
        elif user_message in {"!蒜頭自介", "！蒜頭自介"}:
            message = TextSendMessage(text = introduce_msg)
            line_bot_api.reply_message(event.reply_token, message)
        
        elif user_message.find('請問蒜頭') == 0:
            #event_id = check_group_or_user(event.source)
            reply_msg = chatGPT.get_response(user_message)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_msg))
            #line_bot_api.push_message(event_id, TextSendMessage(text=reply_msg))
        
        # announce to line group
        elif user_message.startswith('！公告 ') or user_message.startswith('!公告 '):
            announce_notify.lineNotifyAnnounce(user_message[4:], announce_token)
        
        # 幹話
        elif user_message == "好美":
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "哪有你美"))
        elif user_message in {"對吧蒜頭", "是吧蒜頭"}:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = "沒錯!!"))
        elif user_message in {"好阿", "好啊", "好"}:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = user_message))
        elif user_message == "!!測試":
            event_id = check_group_or_user(event.source)
            print(event_id)
            #time.sleep(31)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="測試成功!"))
            #line_bot_api.push_message(event_id, TextSendMessage(text="測試成功!"))


