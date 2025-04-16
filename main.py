# -*- coding: utf-8 -*-
#import logging, uvicorn
from datetime import datetime
import os
import json
import random
import asyncio
import threading
import time
from fastapi import FastAPI, Request, HTTPException

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

from Class import chatgpt
from Notify import weather_notify, star_sign_notify
# from Notify import announce_notify

# get env variables
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN',  None))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET',  None))
introduce_msg = os.getenv('INTRODUCE_MESSAGE', None)
cwa_token = os.getenv('CWA_TOKEN', None)

# push message ids
authorized_user = os.getenv('AUTHORIZED_USER', None)
authorized_msg = os.getenv('AUTHORIZED_MSG', None)
announce_group_id = os.getenv('ANNOUNCE_GROUP_ID', None)
specific_notify_id = os.getenv('SPECIFIC_NOTIFY_ID', None)
notify_ids = specific_notify_id.split(',')

# init dictionary
star_sign_map = json.loads(os.getenv('STAR_SIGN_WORDS', None))
star_sign_dict = json.loads(os.getenv('STAR_SIGN_DICT', None))
special_chars = {"!", "！"}

# ====== create golbal loop ===========
global_loop = asyncio.new_event_loop()

def start_loop():
    asyncio.set_event_loop(global_loop)
    global_loop.run_forever()

threading.Thread(target=start_loop, daemon=True).start()
# ====== create golbal loop end =======

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
    future = asyncio.run_coroutine_threadsafe(weather_notify.lineNotifyWeather(cwa_token), global_loop)
    weather_reply = future.result(timeout=15)

    for id in notify_ids:
        line_bot_api.push_message(id, TextSendMessage(text=weather_reply))
    return 'OK'

# Line StarSign Notify
@app.post("/lineNotifyStarSign")
async def lineNotifyStarSign():
    random_star_sign = random.choice(list(star_sign_dict.keys()))
    reply_msg = star_sign_notify.lineNotifyStarSign(random_star_sign, star_sign_dict[random_star_sign])

    for id in notify_ids:
        line_bot_api.push_message(id, TextSendMessage(text=reply_msg))
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
    user_message = str(event.message.text)
    print(user_message)

    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":

        #star sign response
        star_sign = user_message.replace(' ','')
        star_check = False
        if len(star_sign) in {3, 4} and star_sign[0] in special_chars:
            star_sign = star_sign[1:]
            star_check = True
        
        if star_check and len(star_sign) in {2, 3} and star_sign in star_sign_map:
            star_sign = star_sign_map[star_sign]
            star_sign_daily = star_sign_notify.lineNotifyStarSign(star_sign, star_sign_dict[star_sign])
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
            # temp remove for more consider
            if event.source.type == 'group' and event.source.group_id == announce_group_id:
                for id in notify_ids:
                    line_bot_api.push_message(id, TextSendMessage(text=user_message[4:]))
        
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
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="測試成功!"))
            #line_bot_api.push_message(event_id, TextSendMessage(text="測試成功!"))

        elif user_message == authorized_msg:
            event_id = check_group_or_user(event.source)
            print(event_id)
            if event_id not in notify_ids or event.source.user_id != authorized_user:
                print("return by not authorized user")
                return
            future = asyncio.run_coroutine_threadsafe(weather_notify.lineNotifyWeather(cwa_token), global_loop)
            weather_reply = future.result(timeout=15)
            random_star_sign = random.choice(list(star_sign_dict.keys()))
            star_sign_reply = star_sign_notify.lineNotifyStarSign(random_star_sign, star_sign_dict[random_star_sign])
            reply_msg = f"{weather_reply}\n{star_sign_reply}"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = reply_msg))

        elif user_message in {"!今日天氣", "！今日天氣"}:
            print("📦 收到 '今日天氣' 指令")
            try:
                print("call lineNotifyWeather")
                future = asyncio.run_coroutine_threadsafe(weather_notify.lineNotifyWeather(cwa_token), global_loop)
                print(future)
                weather_reply = future.result(timeout=15)
                print(weather_reply)
            except Exception as e:
                print(f"❌ weather_notify 發生錯誤: {e}")
                weather_reply = "目前天氣查詢異常，請稍後再試。"

            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = weather_reply))
