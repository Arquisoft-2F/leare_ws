import requests
from src.config.settings import settings

def send_message(room_id: str, user_id: str, nickname: str, content: str):
    response = requests.post(
        f'{settings.CHAT_MS_URL}/message/{room_id}',
        json={
            "chat_id": room_id,
            "sender_id": user_id,
            "sender_nickname": nickname,
            "content": content
        }
    )
    return response.json()

def edit_message(message_id: str, content: str):
    response = requests.patch(
        f'{settings.CHAT_MS_URL}/message/{message_id}/edit',
        json={
            "content": content
        }
    )
    return response.json()

def delete_message(message_id: str):
    response = requests.delete(
        f'{settings.CHAT_MS_URL}/message/{message_id}'
    )
    return response.json()
