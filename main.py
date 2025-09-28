from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from routes.messages import router as messages_router
from ws_manager import WSManager
from models import MessageOut
from database import insert_message
from datetime import datetime

app = FastAPI(title='Chat Refatorado - FastAPI + MongoDB + WS')

ws_manager = WSManager()

app.include_router(messages_router)

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            sender = data.get('sender')
            content = data.get('content')
            if not sender or not content or not str(content).strip():
                continue
            doc = {
                'sender': sender,
                'content': content,
                'created_at': datetime.utcnow()
            }
            inserted_id = await insert_message(doc)
            doc['_id'] = inserted_id
            payload = MessageOut(**doc).dict(by_alias=True)
            await ws_manager.broadcast(payload)
    except WebSocketDisconnect:
        await ws_manager.disconnect(websocket)
    except Exception:
        await ws_manager.disconnect(websocket)
        raise
