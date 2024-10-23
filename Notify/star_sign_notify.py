import requests
import os
from bs4 import BeautifulSoup

def StarSignDaily(star_sign, serial_no):
    #set url
    star_sign_url = f"https://astro.click108.com.tw/daily_{serial_no}.php?iAstro={serial_no}"
    response = requests.get(star_sign_url)
    response.encoding = 'utf-8'

    # use BeautifulSoup to analyze HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # get element for class="TODAY_CONTENT"
    today_content_elements = soup.find_all(class_="TODAY_CONTENT")

    daily_analysis = '【' + star_sign + '】\n' 
    for element in today_content_elements:
        paragraphs = element.find_all('p')
        for paragraph in paragraphs:
            daily_analysis += paragraph.get_text(strip=True) + '\n'

    if daily_analysis.find("整體運勢") == -1:
        return "媽的找不到星座運勢 八成是星座網頁出問題了 可憐哪!快報修吧"
        
    return daily_analysis

def lineNotifyStarSign(token, star_sign, serial_no):

    # add headers
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"}
    
    msg = '\n' + StarSignDaily(star_sign, serial_no)
    msg += '\n'
    msg += '若要查詢更多星座運勢 \n'
    msg += '請輸入: ! + 星座名 \n'
    msg += '例如: !牡羊座'

    return msg
    # send request
    # res = {'message': msg }

    # if msg.find("媽的找不到星座運勢") >= 0:
    #     myself_token = os.getenv('MYSELF_TOKEN', None)
    #     headers = {
    #         "Authorization": "Bearer " + myself_token,
    #         "Content-Type": "application/x-www-form-urlencoded"}
        
    # response = requests.post("https://notify-api.line.me/api/notify",
    #                   headers=headers, params=res)
