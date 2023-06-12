# FastAPI-linebot-Render-ChatGPT3.5-LineNotify
## 這是一個使用 Python FastAPI 框架創建的 linebot，並建置於 Render 平台上運行，並使用 ChatGPT API 來回覆對話，與結合 LineNotify 來發佈天氣預報。

### 以 Python FastAPI 框架建立 linebot，可參考以下文章之 Sample Code 並進行調整
https://hackmd.io/@CXPhoenix/ryn6ofsGj


### 部屬在 Render 上
1. 到 render 平台上申請帳號並登入：https://render.com/
2. 點選左上角的 "New"，並點選 "Web Service"
3. 可以點選左邊連結到自己 Github 的設定，並選擇要部屬的專案按 Connect，或在下方直接輸入要部屬的專案的 repository url 並按 continue
4. Name 輸入自定義的 Service Name
5. Region 選 Singapore
6. Build Command 預設應該為 "pip install -r requirements.txt" ， 不需更改 
7. Start Command 輸入 "uvicorn main:app --host 0.0.0.0"
8. 按下方的 Advance 設定環境變數
9. 按 Add Environment Variables 來新增環境變數，以此專案來說，需設定LINE_CHANNEL_SECRET、LINE_CHANNEL_ACCESS_TOKEN、OPENAI_API_KEY與相關設定值、LINENOTIFY_TOKEN
10. 按最下方的 Create Web Service 即可開始部屬
11. 部屬完成後，記得將 Service Url 貼到 line developer 的 Webhook URL 上，這個 Linebot 才能順利運作。


### 使用 LineNotify 來發佈天氣預報
1. 申請 LineNotify 發行權杖，可參考 LineNotify 官網：https://notify-bot.line.me/zh_TW/
2. 申請中央氣象局 API，可參考中央氣象局 Opendata API：https://opendata.cwb.gov.tw/dist/opendata-swagger.html
3. 使用 Google Cloud Scheduler 建立工作排程，定期 Call Linebot Weather API 來發送天氣預報
