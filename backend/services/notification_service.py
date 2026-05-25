import logging
import os
from datetime import datetime, timedelta, timezone
from bson import ObjectId
from db.connection import db

logger = logging.getLogger(__name__)

NOTIFICATION_TTL_DAYS = int(os.getenv("NOTIFICATION_TTL_DAYS", "30"))


class NotificationService:

    @staticmethod
    async def create_notifications(user_ids: list, article_id: str, article_title: str, tags: list):
        if not user_ids:
            return
        try:
            from core.fcm import send_push_multicast

            now = datetime.now(timezone.utc)
            docs = [
                {
                    "user_id": uid,
                    "article_id": article_id,
                    "article_title": article_title,
                    "tags": tags,
                    "created_at": now,
                    "is_read": False,
                }
                for uid in user_ids
            ]
            await db.notification.insert_many(docs)

            # Collect FCM tokens for all subscribers
            users = await db.user.find(
                {"_id": {"$in": [ObjectId(uid) for uid in user_ids if ObjectId.is_valid(uid)]},
                 "fcm_token": {"$exists": True, "$ne": None}},
                {"fcm_token": 1}
            ).to_list(length=None)

            tokens = [u["fcm_token"] for u in users if u.get("fcm_token")]
            if tokens:
                tag_str = ", ".join(f"#{t}" for t in tags[:3])
                result = await send_push_multicast(
                    tokens,
                    title="Artikel baru untukmu!",
                    body=f"{article_title} ({tag_str})",
                    data={"article_id": article_id, "tags": ",".join(tags)},
                )
                logger.info("FCM multicast: %s", result)

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
                    "is_read": d.get("is_read", False),
                }
                for d in docs
            ]
        except Exception as e:
            logger.error("get_notifications error: %s", e)
            return []

    @staticmethod
    async def mark_read(notification_id: str, user_id: str) -> bool:
        try:
            result = await db.notification.update_one(
                {"_id": ObjectId(notification_id), "user_id": user_id},
                {"$set": {"is_read": True, "read_at": datetime.now(timezone.utc)}}
            )
            return result.modified_count == 1
        except Exception as e:
            logger.error("mark_read error: %s", e)
            return False

    @staticmethod
    async def mark_all_read(user_id: str) -> int:
        try:
            result = await db.notification.update_many(
                {"user_id": user_id, "is_read": False},
                {"$set": {"is_read": True, "read_at": datetime.now(timezone.utc)}}
            )
            return result.modified_count
        except Exception as e:
            logger.error("mark_all_read error: %s", e)
            return 0
