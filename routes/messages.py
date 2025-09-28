from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from models import MessageIn, MessageOut
from database import insert_message, find_messages
from models import serialize_message

router = APIRouter(prefix="/messages", tags=["messages"])

@router.post('', response_model=MessageOut, status_code=201)
async def create_message(payload: MessageIn):
    
    doc = {
        'sender': payload.sender,
        'content': payload.content,
        'created_at': datetime.utcnow()
    }
    inserted_id = await insert_message(doc)
    doc['_id'] = inserted_id
    return MessageOut(**doc)

@router.get('', response_model=List[MessageOut])
async def list_messages(limit: int = Query(50, ge=1, le=200), before_id: Optional[str] = Query(None)):
    
    filt = {}
    if before_id:
        if not ObjectId.is_valid(before_id):
            raise HTTPException(status_code=400, detail='before_id inválido')
        filt = {'_id': {'$lt': ObjectId(before_id)}}
    docs = await find_messages(limit=limit, before_filter=filt)
    result = []
    for d in docs:
        d['_id'] = d.get('_id')
        result.append(d)
    return [MessageOut(**doc) for doc in result]
