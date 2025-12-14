import os
from motor.motor_asyncio import AsyncIOMotorClient

# Try multiple environment variable names
MONGO_URI = os.getenv("MONGO_URI") or os.getenv("MONGO_URL") or "mongodb://localhost:27017"

print(f"🔍 Connecting to MongoDB: {MONGO_URI[:20]}...")  # Print first 20 chars for debugging

client = AsyncIOMotorClient(MONGO_URI)
db = client["Retogen"]
