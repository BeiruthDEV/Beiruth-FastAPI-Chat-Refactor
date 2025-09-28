from typing import Set
from fastapi import WebSocket
import asyncio
import json

class WSManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        async with self._lock:
            self.active_connections.add(websocket)

    async def disconnect(self, websocket: WebSocket):
        async with self._lock:
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        
        payload = json.dumps(message)
        async with self._lock:
            to_remove = []
            for ws in list(self.active_connections):
                try:
                    await ws.send_text(payload)
                except Exception:
                    to_remove.append(ws)
            for ws in to_remove:
                self.active_connections.discard(ws)
