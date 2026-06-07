"""
Upload semua seed JSON ke MongoDB Atlas.
Usage:
    python db/seed_atlas.py
"""
import asyncio
import json
import os
import sys
import base64
from pathlib import Path
from bson import ObjectId, Binary
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "Retogen")

if not MONGO_URI:
    print("ERROR: Set env var MONGO_URI terlebih dahulu.")
    sys.exit(1)

SEED_DIR = Path(__file__).parent / "seed"

COLLECTIONS = {
    "user":           SEED_DIR / "Retogen.user.json",
    "article":        SEED_DIR / "Retogen.article.json",
    "comment":        SEED_DIR / "Retogen.comment.json",
    "rating":         SEED_DIR / "Retogen.rating.json",
    "report_article": SEED_DIR / "Retogen.report_article.json",
    "report_user":    SEED_DIR / "Retogen.report_user.json",
}


def parse_extended_json(obj):
    """Konversi Extended JSON ($oid, $date, dll) ke tipe Python/BSON."""
    if isinstance(obj, dict):
        if "$oid" in obj:
            return ObjectId(obj["$oid"])
        if "$binary" in obj:
            b64 = obj["$binary"].get("base64", "")
            return Binary(base64.b64decode(b64))
        if "$date" in obj:
            val = obj["$date"]
            if isinstance(val, dict) and "$numberLong" in val:
                ms = int(val["$numberLong"])
                return datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
            if isinstance(val, str):
                return datetime.fromisoformat(val.replace("Z", "+00:00"))
            if isinstance(val, (int, float)):
                return datetime.fromtimestamp(val / 1000, tz=timezone.utc)
        if "$numberLong" in obj:
            return int(obj["$numberLong"])
        if "$numberInt" in obj:
            return int(obj["$numberInt"])
        return {k: parse_extended_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [parse_extended_json(i) for i in obj]
    return obj


async def seed():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[MONGO_DB_NAME]

    for collection_name, json_path in COLLECTIONS.items():
        if not json_path.exists():
            print(f"[SKIP] File tidak ditemukan: {json_path.name}")
            continue

        with open(json_path, encoding="utf-8-sig") as f:
            raw = json.load(f)

        docs = parse_extended_json(raw)
        if not docs:
            print(f"[SKIP] {json_path.name} kosong")
            continue

        collection = db[collection_name]
        inserted = 0
        skipped = 0

        for doc in docs:
            doc_id = doc.get("_id")
            if doc_id and await collection.find_one({"_id": doc_id}):
                skipped += 1
                continue
            await collection.insert_one(doc)
            inserted += 1

        print(f"[OK]   {collection_name}: {inserted} inserted, {skipped} skipped")

    client.close()
    print("\nSelesai! Semua data sudah di MongoDB Atlas.")


if __name__ == "__main__":
    asyncio.run(seed())
