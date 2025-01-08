from fastapi import APIRouter
from .socket.controller import router as socket_router

router = APIRouter()
router.include_router(socket_router)