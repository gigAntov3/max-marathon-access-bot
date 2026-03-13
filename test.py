import requests

from config import settings

headers = {
    'Authorization': settings.bot.token
}

responce = requests.get(
    url='https://platform-api.max.ru/subscriptions',
    headers=headers
)

data = responce.json()



responce = requests.delete(
    url='https://platform-api.max.ru/subscriptions',
    headers=headers,
    params={
        'url': data['subscriptions'][0]['url'],
    }
)

print(responce.json())