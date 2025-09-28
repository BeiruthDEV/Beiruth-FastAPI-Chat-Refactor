from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)

class MessageIn(BaseModel):
    sender: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)

    @validator('sender', 'content')
    def not_blank(cls, v):
        if not v or not v.strip():
            raise ValueError('must not be blank')
        return v.strip()

class MessageOut(BaseModel):
    id: PyObjectId = Field(..., alias='_id')
    sender: str
    content: str
    created_at: datetime

    class Config:
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}
        allow_population_by_field_name = True

def serialize_message(doc: dict) -> dict:
    if not doc:
        return {}
    return {
        '_id': str(doc.get('_id')),
        'sender': doc.get('sender'),
        'content': doc.get('content'),
        'created_at': doc.get('created_at').isoformat() if doc.get('created_at') else None
    }
