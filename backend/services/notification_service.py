import logging
import os
from datetime import datetime, timedelta, timezone
from db.connection import db

logger = logging.getLogger(__name__)

NOTIFICATION_TTL_DAYS = int(os.getenv("NOTIFICATION_TTL_DAYS", "30"))


class NotificationService:

    @staticmethod
    async def create_notifications(user_ids: list, article_id: str, article_title: str, tags: list):
        if not user_ids:
            return
        try:
            now = datetime.now(timezone.utc)
            docs = [
                {
                    "user_id": uid,
                    "article_id": article_id,
                    "article_title": article_title,
                    "tags": tags,
                    "created_at": now,
                }
                for uid in user_ids
            ]
            await db.notification.insert_many(docs)
        except Exception as e:
            logger.error("create_notifications error: %s", e)

    @staticmethod
    async def get_notifications(user_id: str) -> list:
        try:
            cutoff = datetime.now(timezone.utc) - timedelta(days=NOTIFICATION_TTL_DAYS)
            await db.notification.delete_many({
                "user_id": user_id,
                "created_at": {"$lt": cutoff}
            })
            cursor = db.notification.find(
                {"user_id": user_id},
                sort=[("created_at", -1)]
            )
            docs = await cursor.to_list(length=None)
            return [
                {
                    "notification_id": str(d["_id"]),
                    "article_id": d["article_id"],
                    "article_title": d["article_title"],
                    "tags": d["tags"],
                    "created_at": d["created_at"].isoformat(),
                }
                for d in docs
            ]
        except Exception as e:
            logger.error("get_notifications error: %s", e)
            return []
