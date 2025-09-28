from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL, MONGO_DB

client = AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DB]

messages_collection = db.get_collection('messages')

async def insert_message(doc: dict):
    result = await messages_collection.insert_one(doc)
    return result.inserted_id

async def find_messages(limit: int = 50, before_filter: dict = None):
    query = before_filter or {}
    cursor = messages_collection.find(query).sort('_id', -1).limit(limit)
    return await cursor.to_list(length=limit)
