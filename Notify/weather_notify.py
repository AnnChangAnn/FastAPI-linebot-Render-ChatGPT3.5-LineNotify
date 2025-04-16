import httpx
import time

async def lineNotifyWeather(cwa_token: str):
    # set the weather of location
    location_list = ['臺北市', '新北市', '桃園市', '基隆市', '高雄市']
    msg = '【今日天氣】'
    msg += "\r時間: 6:00~18:00\r"
    msg_weather = ''

    for location in location_list:
        print(f"查詢 {location} 天氣中...")

        cwbApiUrl = (
            "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
            f"?Authorization={cwa_token}&locationName={location}"
        )
        print(cwbApiUrl)
        
        response = None
        response = requests.get(cwbApiUrl)

        try:
            data = response.json()
            loc_data = data['records']['location'][0]
            loc_name = loc_data['locationName']
            weather = loc_data['weatherElement'][0]['time'][0]['parameter']['parameterName']
            pop = loc_data['weatherElement'][1]['time'][0]['parameter']['parameterName']
            minT = loc_data['weatherElement'][2]['time'][0]['parameter']['parameterName']
            maxT = loc_data['weatherElement'][4]['time'][0]['parameter']['parameterName']
            msg_weather += f"\n\n{loc_name}: {weather}\n氣溫: {minT}度~{maxT}度\n降雨機率: {pop}%"
        except Exception as e:
            print(f"處理 {location} 資料時出錯: {e}")
            
    return msg + msg_weather + "\n"
