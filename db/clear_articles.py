import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    print("ERROR: Set MONGO_URI terlebih dahulu.")
    sys.exit(1)

async def clear():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client["Retogen"]
    result = await db.article.delete_many({})
    print(f"Deleted {result.deleted_count} articles.")
    client.close()

asyncio.run(clear())
