import requests
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

    daily_analysis = '【' + star_sign + '】今日運勢 \n' 
    for element in today_content_elements:
        paragraphs = element.find_all('p')
        for paragraph in paragraphs:
            daily_analysis += paragraph.get_text(strip=True) + '\n'

    return daily_analysis

def lineNotifyStarSign(star_sign, serial_no):

    # test token : VAH3QdBdbkQ7B9blSEpEpjlwA4GR0MKxzbEHhShkse8
    # add headers
    headers = {
        "Authorization": "Bearer " + "FA9HbhPNUmEg2zgAySH79xP0ySACtxbUOn2GofMZFb0",
        "Content-Type": "application/x-www-form-urlencoded"}
    
    msg = '\n' + StarSignDaily(star_sign, serial_no)
    msg += '\n'
    msg += '若要查詢更多星座運勢 \n'
    msg += '請輸入: ! + 星座名 \n'
    msg += '例如: !牡羊座'

    # send request
    res = {'message': msg }
    response = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=res)