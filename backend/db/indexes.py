import logging
from pymongo import ASCENDING, DESCENDING
from db.connection import db

logger = logging.getLogger(__name__)


async def ensure_indexes():
    """Create all MongoDB indexes. Safe to call on every startup — idempotent."""
    try:
        # user: login + register check by email
        await db.user.create_index([("email", ASCENDING)], unique=True, name="user_email_unique")

        # article: main page listing (filter deleted, sort by date)
        await db.article.create_index(
            [("is_deleted", ASCENDING), ("created_at", DESCENDING)],
            name="article_list"
        )

        # comment: fetch all comments for an article + tree traversal by parent
        await db.comment.create_index([("article_id", ASCENDING)], name="comment_article_id")
        await db.comment.create_index([("parent_comment_id", ASCENDING)], name="comment_parent_id")

        # rating: fetch ratings per article + duplicate check
        await db.rating.create_index([("article_id", ASCENDING)], name="rating_article_id")
        await db.rating.create_index(
            [("article_id", ASCENDING), ("owner_id", ASCENDING)],
            unique=True,
            name="rating_unique_per_user"
        )

        # report_article: fetch reports per article
        await db.report_article.create_index(
            [("article_id", ASCENDING)],
            name="report_article_article_id"
        )

        # report_user: lookup reports by reported user
        await db.report_user.create_index(
            [("reported_user_id", ASCENDING)],
            name="report_user_reported_id"
        )

        # subscription: lookup by user
        await db.subscription.create_index([("user_id", ASCENDING)], name="subscription_user_id")

        # notification: fetch + TTL cleanup per user
        await db.notification.create_index(
            [("user_id", ASCENDING), ("created_at", DESCENDING)],
            name="notification_user_created"
        )

        logger.info("MongoDB indexes ensured.")
    except Exception as e:
        logger.error("ensure_indexes error: %s", e)
