import logging
import os
from datetime import datetime, timedelta, timezone
from bson import ObjectId
from db.connection import db

logger = logging.getLogger(__name__)

NOTIFICATION_TTL_DAYS = int(os.getenv("NOTIFICATION_TTL_DAYS", "30"))

# ---------------------------------------------------------------------------
# Firebase Admin — optional, only initialised when credentials file exists
# ---------------------------------------------------------------------------
_firebase_ready = False


def _init_firebase():
    global _firebase_ready
    if _firebase_ready:
        return True

    creds_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase_credentials.json")
    if not os.path.exists(creds_path):
        logger.info("Firebase credentials not found at '%s'. FCM push disabled.", creds_path)
        return False

    try:
        import firebase_admin
        from firebase_admin import credentials
        if not firebase_admin._apps:
            cred = credentials.Certificate(creds_path)
            firebase_admin.initialize_app(cred)
        _firebase_ready = True
        logger.info("Firebase Admin SDK initialised.")
        return True
    except Exception as e:
        logger.error("Firebase init error: %s", e)
        return False


async def _send_fcm(tokens: list[str], title: str, body: str):
    """Send FCM multicast push. Silently skipped if Firebase not configured."""
    if not tokens:
        return
    if not _init_firebase():
        return
    try:
        from firebase_admin import messaging
        response = messaging.send_each_for_multicast(
            messaging.MulticastMessage(
                notification=messaging.Notification(title=title, body=body),
                tokens=tokens,
            )
        )
        logger.info("FCM: %d sent, %d failed", response.success_count, response.failure_count)
    except Exception as e:
        logger.error("FCM send error: %s", e)


# ---------------------------------------------------------------------------
# NotificationService
# ---------------------------------------------------------------------------

class NotificationService:

    @staticmethod
    async def register_fcm_token(user_id: str, token: str) -> bool:
        """Save or update the FCM device token for a user."""
        try:
            await db.user.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"fcm_token": token}},
            )
            return True
        except Exception as e:
            logger.error("register_fcm_token error: %s", e)
            return False

    @staticmethod
    async def create_notifications(
        user_ids: list, article_id: str, article_title: str, tags: list
    ):
        """
        1. Write in-app notification docs to DB.
        2. Send FCM push to users who have a registered device token.
        """
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

            # Collect FCM tokens for push notifications
            try:
                oids = [ObjectId(uid) for uid in user_ids]
            except Exception:
                return

            users = await db.user.find(
                {"_id": {"$in": oids}, "fcm_token": {"$exists": True, "$ne": None}}
            ).to_list(length=None)

            tokens = [u["fcm_token"] for u in users if u.get("fcm_token")]
            tag_line = f"Tag: {', '.join(tags)}" if tags else "Artikel baru di RetoGen"
            await _send_fcm(tokens, article_title, tag_line)

        except Exception as e:
            logger.error("create_notifications error: %s", e)

    @staticmethod
    async def get_notifications(user_id: str) -> list:
        try:
            cutoff = datetime.now(timezone.utc) - timedelta(days=NOTIFICATION_TTL_DAYS)
            await db.notification.delete_many({
                "user_id": user_id,
                "created_at": {"$lt": cutoff},
            })
            cursor = db.notification.find(
                {"user_id": user_id},
                sort=[("created_at", -1)],
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
