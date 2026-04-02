import logging
from db.connection import db

logger = logging.getLogger(__name__)

MAX_SUBSCRIPTIONS = 20


class SubscriptionService:

    @staticmethod
    async def subscribe(user_id: str, tag: str) -> str:
        try:
            sub = await db.subscription.find_one({"user_id": user_id})
            if sub:
                if tag in sub.get("tags", []):
                    return "already subscribed"
                if len(sub.get("tags", [])) >= MAX_SUBSCRIPTIONS:
                    return "limit reached"
                await db.subscription.update_one(
                    {"user_id": user_id},
                    {"$addToSet": {"tags": tag}}
                )
            else:
                await db.subscription.insert_one({"user_id": user_id, "tags": [tag]})
            return "subscribed"
        except Exception as e:
            logger.error("subscribe error: %s", e)
            return "error"

    @staticmethod
    async def unsubscribe(user_id: str, tag: str) -> str:
        try:
            result = await db.subscription.update_one(
                {"user_id": user_id},
                {"$pull": {"tags": tag}}
            )
            if result.modified_count == 0:
                return "not subscribed"
            return "unsubscribed"
        except Exception as e:
            logger.error("unsubscribe error: %s", e)
            return "error"

    @staticmethod
    async def get_subscriptions(user_id: str) -> list:
        try:
            sub = await db.subscription.find_one({"user_id": user_id})
            return sub.get("tags", []) if sub else []
        except Exception as e:
            logger.error("get_subscriptions error: %s", e)
            return []

    @staticmethod
    async def get_subscribers_for_tags(tags: list) -> list:
        try:
            cursor = db.subscription.find({"tags": {"$in": tags}})
            subs = await cursor.to_list(length=None)
            return [s["user_id"] for s in subs]
        except Exception as e:
            logger.error("get_subscribers_for_tags error: %s", e)
            return []
