import requests
from bs4 import BeautifulSoup

# star sign array
# star_sign = [['0','牡羊座'], ['1','金牛座'], ['2','雙子座'], ['3','巨蟹座'],
#              ['4','獅子座'], ['5','處女座'], ['6','天秤座'], ['7','天蠍座'],
#              ['8','射手座'], ['9','摩羯座'], ['10','水瓶座'], ['11','雙魚座'],
#              ['2','双子座'], ['6','天平座'], ['6','天枰座'],  ['9','魔羯座'], 
#              ['10','水平座'], ['11','双魚座']]

# # 請求獲取網頁HTML內容
# for star in star_sign:
#     star_sign_url = f"https://astro.click108.com.tw/daily_{star[0]}.php?iAstro={star[0]}"
#     response = requests.get(star_sign_url)
#     response.encoding = 'utf-8'

#     # 使用BeautifulSoup解析HTML內容
#     soup = BeautifulSoup(response.text, 'html.parser')

#     # 查找所有class為 "TODAY_CONTENT" 的元素
#     today_content_elements = soup.find_all(class_="TODAY_CONTENT")

#     # 單獨打印每個元素內每個<p>標籤的文本內容，並加上換行
#     print('【' + star[1] + '】')
#     for element in today_content_elements:
#         paragraphs = element.find_all('p')
#         for paragraph in paragraphs:
#             print(paragraph.get_text(strip=True))
#     print('\n')

def star_sign_daily(star_sign, serial_no):
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