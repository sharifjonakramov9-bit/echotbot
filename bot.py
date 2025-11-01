import json
import requests
from config import TOKEN

TG_BOT_URL = f'https://api.telegram.org/bot{TOKEN}'


def get_updates(offset: int | None, limit: int = 100):
    url = f'{TG_BOT_URL}/getUpdates'
    params = {
        'offset': offset,
        'limit': limit
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()['result']
    
def send_message(chat_id: int | str, text: str):
    url = f'{TG_BOT_URL}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': text
    }
    requests.get(url, params=params)
    
def send_photo(chat_id: int | str, photo: str):
    url = f'{TG_BOT_URL}/sendPhoto'
    params = {
        'chat_id': chat_id,
        'photo': photo
    }
    requests.get(url, params=params)
    
def send_location(chat_id: int | str, latitude: float, longitude: float):
    url = f'{TG_BOT_URL}/sendLocation'
    params = {
        'chat_id': chat_id,
        'latitude': latitude,
        'longitude': longitude,
    }
    requests.get(url, params=params)

def save_user(user_data: dict):
    with open('users.json', 'r') as f:
        users = json.load(f)

    for user in users:
        if user['tg_id'] == user_data['tg_id']:
            return None

    users.append(user_data)

    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

    return user_data

def main():
    offset = None
    limit = 100

    while True:
        for update in get_updates(offset, limit):
            if 'message' in update:
                chat_id = update['message']['chat']['id']

                if 'text' in update['message']:
                    text = update['message']['text']
                    user = update['message']['from']
                    if text == '/start':
                        new_user = {
                            'tg_id': user['id'],
                            'first_name': user['first_name'],
                            'last_name': user.get('last_name'),
                            'username': user.get('username')
                        }
                        new_user = save_user(new_user)
                        text = 'salom, botga xush kelibsiz!'
                        if new_user is None:
                            text = 'salom, qaytganingiz bilan!'

                    send_message(chat_id, text)
                elif 'photo' in update['message']:
                    photo = update['message']['photo'][-1]
                    send_photo(chat_id, photo['file_id'])
                elif 'location' in update['message']:
                    location = update['message']['location']
                    send_location(chat_id, location['latitude'], location['longitude'])

            offset = update['update_id'] + 1

main()
