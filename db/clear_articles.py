"""
Kosongkan semua dokumen di setiap collection (collection tetap ada).
Usage:
    MONGO_URI=<uri> python db/clear_articles.py
"""
import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    print("ERROR: Set MONGO_URI terlebih dahulu.")
    sys.exit(1)

COLLECTIONS = ["article", "user", "comment", "notification", "subscription", "tag", "rating", "report_article", "report_user"]

async def clear_all():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client["Retogen"]
    for col in COLLECTIONS:
        result = await db[col].delete_many({})
        print(f"  {col}: {result.deleted_count} dokumen dihapus")
    client.close()
    print("Selesai.")

asyncio.run(clear_all())
