import requests, json
from datetime import datetime

def lineNotifyWeather(token):

    # test token : VAH3QdBdbkQ7B9blSEpEpjlwA4GR0MKxzbEHhShkse8
    # add headers
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"}
    
    # get now time
    # NowDate = datetime.now().strftime('%Y-%m-%d')
    # print(NowDate)

    # set the weather of location
    Location_List = ['臺北市', '新北市', '桃園市', '基隆市', '高雄市']
    msg = "\r    時間: 6:00~18:00\r"
    msg_weather = ''

    for i in Location_List[0:]:
        # 氣象局改名為氣象署 cwb => cwa
        cwbapi = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-E74B046A-CAB4-4570-B4D9-FA3F7F225DC1&locationName={i}&startTime="
        cwbr = requests.get(cwbapi)
        print('request success!!')

        cwbr_dict = cwbr.json()
        json_string = json.dumps(cwbr_dict)
        json_format = json.loads(json_string)
        location = json_format['records']['location'][0]['locationName']
        weather = json_format['records']['location'][0]['weatherElement'][0]['time'][0]['parameter']['parameterName']
        MinT = json_format['records']['location'][0]['weatherElement'][2]['time'][0]['parameter']['parameterName']
        MaxT = json_format['records']['location'][0]['weatherElement'][4]['time'][0]['parameter']['parameterName']
        pop = json_format['records']['location'][0]['weatherElement'][1]['time'][0]['parameter']['parameterName']
        msg_weather = msg_weather + f'''
        
    {location}: {weather}
    氣溫: {MinT}度~{MaxT}度
    降雨機率: {pop}%'''

    # send request
    res = {'message': msg + msg_weather}
    response = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=res)
