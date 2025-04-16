import requests
from datetime import datetime
import time

def lineNotifyWeather(cwa_token):
    # set the weather of location
    Location_List = ['臺北市', '新北市', '桃園市', '基隆市', '高雄市']
    msg = '【今日天氣】'
    msg += "\r時間: 6:00~18:00\r"
    msg_weather = ''

    for i in Location_List[0:]:
        # 氣象局改名為氣象署 cwb => cwa
        print("call cwa api...")
        cwbapi = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={cwa_token}&locationName={i}"
        # cwbr = requests.get(cwbapi)

        for attempt in range(3):  # 最多 retry 三次
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    break
                else:
                    print(f"錯誤狀態碼：{response.status_code}，重試中...")
            except requests.exceptions.RequestException as e:
                print(f"連線錯誤：{e}，重試中...")
                time.sleep(0.1)
        # cwbr_dict = cwbr.json()
        # json_string = json.dumps(cwbr_dict)
        # json_format = json.loads(json_string)
        json_format = response.json()
        location = json_format['records']['location'][0]['locationName']
        weather = json_format['records']['location'][0]['weatherElement'][0]['time'][0]['parameter']['parameterName']
        MinT = json_format['records']['location'][0]['weatherElement'][2]['time'][0]['parameter']['parameterName']
        MaxT = json_format['records']['location'][0]['weatherElement'][4]['time'][0]['parameter']['parameterName']
        pop = json_format['records']['location'][0]['weatherElement'][1]['time'][0]['parameter']['parameterName']
        msg_weather += f"\n\n{location}: {weather}\n氣溫: {MinT}度~{MaxT}度\n降雨機率: {pop}%"

    return msg + msg_weather + ' \n '
