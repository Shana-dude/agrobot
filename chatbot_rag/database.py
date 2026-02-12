import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/agrobot")
client = AsyncIOMotorClient(MONGO_URI)
db = client.get_database()
chat_collection = db.chat_history

async def save_chat(query: str, answer: str):
    chat_entry = {
        "query": query,
        "answer": answer,
        "timestamp": datetime.utcnow()
    }
    await chat_collection.insert_one(chat_entry)

async def get_recent_chats(limit: int = 10):
    chats = []
    cursor = chat_collection.find().sort("timestamp", -1).limit(limit)
    async for document in cursor:
        document["_id"] = str(document["_id"])
        chats.append(document)
    return chats
