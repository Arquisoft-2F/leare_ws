from fastapi import WebSocket
from src.utils.connectionManager import ConnectionManager
from src.utils.api_requests import send_message, edit_message, delete_message

class ChatWebSocketController:
    manager = ConnectionManager()

    @classmethod
    async def connect(cls, websocket: WebSocket, room_id: str):
        return await cls.manager.connect(websocket, room_id)

    @classmethod
    async def disconnect(cls, connection_id: str, room_id: str, nickname: str):
        cls.manager.disconnect(connection_id, room_id)
        await cls.manager.broadcast({
            "type": "disconnect",
            "connection_id": connection_id,
            "nickname": nickname,
        }, room_id, exclude_connection_id=connection_id)

    @classmethod
    async def send_message(cls, connection_id: str, room_id: str, user_id: str, nickname: str, content: str, created_at: str):
        msg = send_message(room_id, user_id, nickname, content)
        message = {
            "type": "message_sent",
            "id": str(msg["id"]),
            "content": content,
            "sender_id": user_id,
            "sender_nickname": nickname,
            "created_at": created_at
        }
        await cls.manager.broadcast(message, room_id=room_id)

    @classmethod
    async def edit_message(cls, connection_id: str, room_id: str, message_id: str, content: str):
        edit_message(message_id, content)
        message = {
            "type": "message_edited",
            "id": message_id,
            "content": content
        }
        await cls.manager.broadcast(message, room_id=room_id, exclude_connection_id=connection_id)

    @classmethod
    async def delete_message(cls, connection_id: str, room_id: str, message_id: str):
        delete_message(message_id)
        message = {
            "type": "message_deleted",
            "id": message_id
        }
        await cls.manager.broadcast(message, room_id=room_id, exclude_connection_id=connection_id)
