"""
Database configuration and connection setup using Motor.
"""
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = AsyncIOMotorClient(settings.MONGODB_URI)
database = client[settings.MONGODB_NAME]
clients_collection = database.get_collection("clients")
