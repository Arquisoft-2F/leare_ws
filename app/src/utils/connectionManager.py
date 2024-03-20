import uuid
from fastapi import WebSocket

class ChatRoom:
    def __init__(self, room_id: str):
        self.room_id = room_id
        self.active_connections = {}
    
    def add_connection(self, connection_id: str, websocket: WebSocket) -> None:
        self.active_connections[connection_id] = websocket
    
    def remove_connection(self, connection_id: str) -> None:
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]

    async def broadcast(self, message: dict, exclude_connection_id: str = None) -> None:
        for connection_id, connection in self.active_connections.items():
            if connection_id != exclude_connection_id:
                await connection.send_json(message)

class ConnectionManager:
    def __init__(self):
        self.rooms = {}

    def get_room(self, room_id: str) -> ChatRoom:
        if room_id not in self.rooms:
            self.rooms[room_id] = ChatRoom(room_id)
        return self.rooms[room_id]

    async def connect(self, websocket: WebSocket, room_id: str) -> tuple[str, str]:
        room = self.get_room(room_id)
        connection_id = str(uuid.uuid4())

        await websocket.accept()
        room.add_connection(connection_id, websocket)

        return connection_id, room_id

    def disconnect(self, connection_id: str, room_id: str) -> None:
        room = self.get_room(room_id)
        room.remove_connection(connection_id)

    async def send_personal_message(self, message: dict, connection_id: str, room_id: str) -> None:
        room = self.get_room(room_id)
        websocket = room.active_connections.get(connection_id)
        if websocket:
            await websocket.send_json(message)

    async def broadcast(self, message: dict, room_id: str, exclude_connection_id: str = None) -> None:
        room = self.get_room(room_id)
        await room.broadcast(message, exclude_connection_id)