# -*- coding: utf-8 -*-

import logging, uvicorn
import openai, os
import json
from fastapi import FastAPI, Request, HTTPException

from linebot import LineBotApi, WebhookHandler

from linebot.exceptions import InvalidSignatureError
from linebot.models import *


line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN',  None))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET',  None))
openai.api_key = os.getenv('OPENAI_APIKEY', None)
weather_token = os.getenv('WEATHER_TOKEN', None)


class ChatGPT:  
    def __init__(self):
        self.model = os.getenv("OPENAI_MODEL", default = "gpt-3.5-turbo")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", default = 1.0))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default = 2000))

    def get_response(self, message):
        prompt = message[4:]
        response = openai.ChatCompletion.create(
	            model = self.model,
                messages = [
                    {'role': 'user', 'content': prompt}
                ],
                temperature = self.temperature,
                max_tokens = self.max_tokens
                )
        reply_msg = response['choices'][0]['message']['content'].strip()
        print('AI回答內容' + reply_msg)

        return reply_msg


def check_group_or_user(eventsource):
    if hasattr(eventsource, "group_id"):
        return eventsource.group_id
    else:
        return eventsource.user_id


chatgpt = ChatGPT()
app = FastAPI()
# Line Bot config

@app.get("/") # 指定 api 路徑 (get方法)
async def hello():
	return "Hello World for AnnChangAnn!!"

@app.post("/callback")
async def callback(request: Request):
    signature = request.headers["X-Line-Signature"]
    body = await request.body()
    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Missing Parameters")
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handling_message(event):
    #replyToken = event.reply_token
    user_message = str(event.message.text)
    print(user_message)
    
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        if user_message.find('請問蒜頭') == 0:
            event_id = check_group_or_user(event.source)
            reply_msg = chatgpt.get_response(user_message)
            line_bot_api.push_message(event_id, TextSendMessage(text=reply_msg))

