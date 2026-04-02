import logging
from db.connection import db
from bson import ObjectId, Binary
from utils.image_validator import validate_image_bytes
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class ArticleService:

    @staticmethod
    async def fetch_article(article_id: str):
        try:
            return await db.article.find_one({
                "_id": ObjectId(article_id),
                "is_deleted": False
            })
        except Exception as e:
            logger.error("fetch_article error: %s", e)
            return None

    @staticmethod
    async def update_article(data, image_bytes: bytes):
        update_fields = {}

        if data.article_title is not None:
            update_fields["article_title"] = data.article_title
        if data.article_preview is not None:
            update_fields["article_preview"] = data.article_preview
        if data.article_content is not None:
            update_fields["article_content"] = data.article_content
        if data.article_tags is not None:
            update_fields["article_tags"] = [t.strip().lower() for t in data.article_tags]

        if image_bytes is not None:
            if not validate_image_bytes(image_bytes):
                return "invalid_image"
            update_fields["article_image"] = Binary(image_bytes)

        update_fields["updated_at"] = datetime.now(timezone.utc)

        try:
            result = await db.article.update_one(
                {"_id": ObjectId(data.article_id)},
                {"$set": update_fields}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error("update_article error: %s", e)
            return False

    @staticmethod
    async def add_article(title, preview, content, tags, image_bytes, author_id):
        try:
            now = datetime.now(timezone.utc)
            doc = {
                "article_title": title,
                "article_preview": preview,
                "article_content": content,
                "article_tags": [t.strip().lower() for t in tags],
                "article_image": Binary(image_bytes) if image_bytes else None,
                "author_id": author_id,
                "report_count": 0,
                "created_at": now,
                "updated_at": now,
                "is_deleted": False
            }
            result = await db.article.insert_one(doc)
            if result.inserted_id:
                return str(result.inserted_id)
            return None
        except Exception as e:
            logger.error("add_article error: %s", e)
            return None

    @staticmethod
    async def get_articles_filtered(sort: str, tag: str = None, search: str = None):
        try:
            match = {"is_deleted": False}

            if tag:
                match["article_tags"] = tag.strip().lower()
            if search:
                match["article_title"] = {"$regex": search, "$options": "i"}

            if sort in ("newest", "oldest", "most_reported", "by_tag", "search_title"):
                sort_field = {
                    "newest": ("created_at", -1),
                    "oldest": ("created_at", 1),
                    "most_reported": ("report_count", -1),
                    "by_tag": ("article_tags", 1),
                    "search_title": ("article_title", 1),
                }[sort]

                cursor = db.article.find(match).sort(sort_field[0], sort_field[1])
                return await cursor.to_list(length=None)

            if sort == "highest_rated":
                pipeline = [
                    {"$match": match},
                    {"$addFields": {"article_id_str": {"$toString": "$_id"}}},
                    {"$lookup": {
                        "from": "rating",
                        "localField": "article_id_str",
                        "foreignField": "article_id",
                        "as": "ratings"
                    }},
                    {"$addFields": {"avg_rating": {"$avg": "$ratings.rating_value"}}},
                    {"$sort": {"avg_rating": -1}},
                    {"$project": {"ratings": 0, "article_id_str": 0}}
                ]
                return await db.article.aggregate(pipeline).to_list(length=None)

            if sort == "most_commented":
                pipeline = [
                    {"$match": match},
                    {"$addFields": {"article_id_str": {"$toString": "$_id"}}},
                    {"$lookup": {
                        "from": "comment",
                        "localField": "article_id_str",
                        "foreignField": "article_id",
                        "as": "comments"
                    }},
                    {"$addFields": {"comment_count": {"$size": "$comments"}}},
                    {"$sort": {"comment_count": -1}},
                    {"$project": {"comments": 0, "article_id_str": 0}}
                ]
                return await db.article.aggregate(pipeline).to_list(length=None)

            cursor = db.article.find(match).sort("created_at", -1)
            return await cursor.to_list(length=None)

        except Exception as e:
            logger.error("get_articles_filtered error: %s", e)
            return None
