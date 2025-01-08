from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

from .socket_manager import ConnectionManager

router = APIRouter()


@router.websocket("/ws/{name}")
async def websocket_endpoint(websocket: WebSocket, name: str, client_id: str, manager = Depends(ConnectionManager)):
    await manager.connect(websocket, name, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received: {data}")
            await manager.broadcast(name, f"{client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, name, client_id)

