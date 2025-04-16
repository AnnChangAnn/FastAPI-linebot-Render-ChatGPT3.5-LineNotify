import requests, json
from datetime import datetime

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
        cwbr = requests.get(cwbapi)

        print(f"get response : {cwbr}")
        cwbr_dict = cwbr.json()
        json_string = json.dumps(cwbr_dict)
        json_format = json.loads(json_string)
        print(f"get response : {json_format}")
        location = json_format['records']['location'][0]['locationName']
        print(f"location : {location}")
        weather = json_format['records']['location'][0]['weatherElement'][0]['time'][0]['parameter']['parameterName']
        print(f"weather : {weather}")
        MinT = json_format['records']['location'][0]['weatherElement'][2]['time'][0]['parameter']['parameterName']
        print(f"MinT : {MinT}")
        MaxT = json_format['records']['location'][0]['weatherElement'][4]['time'][0]['parameter']['parameterName']
        print(f"MinT : {MaxT}")
        pop = json_format['records']['location'][0]['weatherElement'][1]['time'][0]['parameter']['parameterName']
        print(f"MinT : {pop}")
        msg_weather += f"\n\n{location}: {weather}\n氣溫: {MinT}度~{MaxT}度\n降雨機率: {pop}%"
        print(f"msg_weather : {msg_weather}")

    return msg + msg_weather + ' \n '
