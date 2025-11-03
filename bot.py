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
                message = update['message']

                if 'text' in message and message['text'] == '/start':
                    user = message['from']
                    new_user = {
                        'tg_id': user['id'],
                        'first_name': user['first_name'],
                        'last_name': user.get('last_name'),
                        'username': user.get('username')
                    }
                    new_user = save_user(new_user)

                    text = 'Salom, botga xush kelibsiz!' if new_user else 'Salom, qaytganingiz bilan!'
                    send_message(chat_id, text)

                elif 'text' in message:
                    send_message(chat_id, message['text'])

                elif 'photo' in message:
                    photo = message['photo'][-1]['file_id']
                    send_photo(chat_id, photo)

                elif 'sticker' in message:
                    sticker = message['sticker']['file_id']
                    requests.get(f"{TG_BOT_URL}/sendSticker?chat_id={chat_id}/sticker={sticker}")

                elif 'voice' in message:
                    voice = message['voice']['file_id']
                    requests.get(f"{TG_BOT_URL}/sendVoice?chat_id={chat_id}/voice={voice}")

                elif 'audio' in message:
                    audio = message['audio']['file_id']
                    requests.get(f"{TG_BOT_URL}/sendAudio?chat_id={chat_id}/audio={audio}")

                elif 'document' in message:
                    document = message['document']['file_id']
                    requests.get(f"{TG_BOT_URL}/sendDocument?chat_id={chat_id}/document={document}")

                elif 'video' in message:
                    video = message['video']['file_id']
                    requests.get(f"{TG_BOT_URL}/sendVideo?chat_id={chat_id}/video={video}")

                elif 'contact' in message:
                    contact = message['contact']
                    requests.get(
                        f"{TG_BOT_URL}/sendContact?chat_id={chat_id}/phone_number={contact['phone_number']}/first_name={contact['first_name']}"
                    )

                elif 'dice' in message:
                    requests.get(f"{TG_BOT_URL}/sendDice?chat_id={chat_id}")

            offset = update['update_id'] + 1

main()
