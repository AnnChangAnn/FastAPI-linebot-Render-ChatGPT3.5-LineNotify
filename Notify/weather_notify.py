# import requests
#from datetime import datetime
#import time
import httpx
import asyncio

async def lineNotifyWeather(cwa_token: str):
    # set the weather of location
    Location_List = ['臺北市', '新北市', '桃園市', '基隆市', '高雄市']
    msg = '【今日天氣】'
    msg += "\r時間: 6:00~18:00\r"
    msg_weather = ''

    headers = {
        "accept": "application/json"
    }

    async with httpx.AsyncClient(timeout=30) as client:
        for i in Location_List:
            # 氣象局改名為氣象署 cwb => cwa
            print(f"🔍 查詢 {i} 天氣中...")
            cwbapi = ( 
                "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
                f"?Authorization={cwa_token}&locationName={i}"
            )
            # cwbr = requests.get(cwbapi)

            try:
                response = await client.get(cwbapi, headers=headers)
                response.raise_for_status()
                json_format = response.json()

                location = json_format['records']['location'][0]['locationName']
                weather = json_format['records']['location'][0]['weatherElement'][0]['time'][0]['parameter']['parameterName']
                MinT = json_format['records']['location'][0]['weatherElement'][2]['time'][0]['parameter']['parameterName']
                MaxT = json_format['records']['location'][0]['weatherElement'][4]['time'][0]['parameter']['parameterName']
                pop = json_format['records']['location'][0]['weatherElement'][1]['time'][0]['parameter']['parameterName']
                msg_weather += f"\n\n{location}: {weather}\n氣溫: {MinT}度~{MaxT}度\n降雨機率: {pop}%"

            except Exception as e:
                print(f"⚠️ 錯誤（{i}）：{e}")
                
    return msg + msg_weather + ' \n '
