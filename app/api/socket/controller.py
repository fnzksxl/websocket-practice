from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

from .socket_manager import ConnectionManager

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, client_id: str, manager = Depends(ConnectionManager)):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received: {data}")
            await manager.broadcast(f"Client{client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(client_id)