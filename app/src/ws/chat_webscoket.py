from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.controllers.wsController import ChatWebSocketController

ws = APIRouter()

@ws.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    connection_id, room_id = await ChatWebSocketController.connect(websocket, room_id)
    try: 
        while True:
            message_data = await websocket.receive_json()

            if message_data["type"] == "user_connected":
                nickname = message_data["user_nickname"]
                user_id = message_data["user_id"]

            elif message_data["type"] == "message_sent":
                nickname = message_data["user_nickname"]
                user_id = message_data["user_id"]
                content = message_data["content"]
                created_at = message_data["created_at"]
                await ChatWebSocketController.send_message(connection_id, room_id, user_id, nickname, content, created_at)

            elif message_data["type"] == "message_edited":
                message_id = message_data["message_id"]
                content = message_data["content"]
                await ChatWebSocketController.edit_message(connection_id, room_id, message_id, content)

            elif message_data["type"] == "message_deleted":
                message_id = message_data["message_id"]
                await ChatWebSocketController.delete_message(connection_id, room_id, message_id)

    except WebSocketDisconnect:
        await ChatWebSocketController.disconnect(connection_id, room_id, nickname)