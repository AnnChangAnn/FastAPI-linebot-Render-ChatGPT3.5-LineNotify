import requests

def lineNotifyAnnounce(message, token):

    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type" : "application/x-www-form-urlencoded"}

    payload = {'message': message}
    response = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)