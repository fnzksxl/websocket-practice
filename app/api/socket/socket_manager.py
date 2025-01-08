from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        del self.active_connections[client_id]
        print(f"Client{client_id} disconnected")

    async def broadcast(self, message: str):
        for websocket in self.active_connections.values():
            await websocket.send_text(message)