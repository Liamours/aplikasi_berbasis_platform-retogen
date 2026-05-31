"""
Production seed script.
Seeds admin user + optional demo articles into any MongoDB URI.

Usage:
    MONGO_URI="mongodb+srv://..." python db/seed_prod.py
    MONGO_URI="mongodb+srv://..." python db/seed_prod.py --admin-only

Does NOT seed comments/ratings/reports — those are test/demo data only.
Safe to re-run: skips records that already exist (no duplicates).
"""
import asyncio
import os
import sys
import argparse
from datetime import datetime, timezone

from motor.motor_asyncio import AsyncIOMotorClient
import bcrypt

MONGO_URI = os.getenv("MONGO_URI") or os.getenv("MONGO_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "Retogen")

if not MONGO_URI:
    print("ERROR: MONGO_URI or MONGO_URL env var required.")
    sys.exit(1)


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


ADMIN_USER = {
    "username": "superadmin",
    "fullname": "Super Admin",
    "email": "admin@retogen.app",
    "password": hash_password("Admin1234"),   # change after first login
    "role": "admin",
    "report_count": 0,
    "created_at": datetime.now(timezone.utc),
    "updated_at": datetime.now(timezone.utc),
}

DEMO_ARTICLES = [
    {
        "article_title": "Dell XPS 15 Review",
        "article_preview": "In-depth look at the Dell XPS 15 9530 performance and build quality.",
        "article_content": "The Dell XPS 15 9530 delivers exceptional performance...",
        "article_tags": ["laptop", "dell", "review"],
        "product_name": "Dell XPS 15 9530",
        "is_deleted": False,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    },
    {
        "article_title": "MacBook Pro 14 Analysis",
        "article_preview": "Comprehensive analysis of the MacBook Pro 14 M3 chip.",
        "article_content": "Apple M3 chip raises the bar for laptop performance...",
        "article_tags": ["laptop", "apple", "review"],
        "product_name": "MacBook Pro 14 M3",
        "is_deleted": False,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    },
]


async def seed(admin_only: bool = False):
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[MONGO_DB_NAME]

    # --- Admin user ---
    existing = await db.user.find_one({"email": ADMIN_USER["email"]})
    if existing:
        print(f"[SKIP] Admin user already exists: {ADMIN_USER['email']}")
    else:
        await db.user.insert_one(ADMIN_USER.copy())
        print(f"[OK]   Admin user created: {ADMIN_USER['email']} / Admin1234")
        print("       IMPORTANT: Change this password immediately after first login.")

    if admin_only:
        print("--admin-only flag set. Skipping demo articles.")
        client.close()
        return

    # --- Demo articles (attach to admin user) ---
    admin = await db.user.find_one({"email": ADMIN_USER["email"]})
    admin_id = str(admin["_id"])

    for art in DEMO_ARTICLES:
        existing = await db.article.find_one({"article_title": art["article_title"]})
        if existing:
            print(f"[SKIP] Article already exists: {art['article_title']}")
        else:
            doc = {**art, "owner_id": admin_id, "owner_username": ADMIN_USER["username"]}
            await db.article.insert_one(doc)
            print(f"[OK]   Article inserted: {art['article_title']}")

    client.close()
    print("\nDone. Ensure indexes are applied by starting the backend once.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--admin-only", action="store_true", help="Only seed admin user, skip articles")
    args = parser.parse_args()
    asyncio.run(seed(admin_only=args.admin_only))
