from fastapi import WebSocket
from collections import defaultdict

from .redis import RedisConnectionPool

redis_pool = RedisConnectionPool()
chat_rooms = defaultdict(list)


class ConnectionManager:
    def __init__(self):
        self.redis = redis_pool.get_redis_client()

    async def connect(self, websocket: WebSocket, name: str, client_id: str):
        await websocket.accept()
        chat_rooms[name].append(websocket)
        if not self.redis.exists(f"chat_room:{name}"):
            self.redis.sadd(f"chat_room:{name}", client_id)
            await websocket.send_text(f"Room {name} has been created.")
        else:
            self.redis.sadd(f"chat_room:{name}", client_id)

        await self.broadcast(name, f"{client_id} has joined room {name}.")

    def disconnect(self, websocket: WebSocket, name: str, client_id: str):
        chat_rooms[name] = [ws for ws in chat_rooms[name] if ws != websocket]
        self.redis.srem(f"chat_room:{name}", int(client_id))
        print(f"Client{client_id} disconnected")

    async def broadcast(self, name: str, message: str):
        for ws in chat_rooms[name]:
            await ws.send_text(message)