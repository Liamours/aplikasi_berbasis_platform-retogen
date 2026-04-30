import logging
from db.connection import db
from bson import ObjectId
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class ReportArticleService:

    @staticmethod
    async def add_report(article_id: str, description: str, owner_id: str):
        try:
            data = {
                "article_id": ObjectId(article_id),
                "owner_id": owner_id,
                "description": description,
                "created_at": datetime.now(timezone.utc)
            }

            result = await db.report_article.insert_one(data)

            await db.article.update_one(
                {"_id": ObjectId(article_id)},
                {"$inc": {"report_count": 1}}
            )

            return str(result.inserted_id)

        except Exception as e:
            logger.error("add_report error: %s", e)
            return None

    @staticmethod
    async def get_reports_by_article(article_id: str):
        try:
            reports_raw = await db.report_article.find({
                "article_id": ObjectId(article_id)
            }).sort("created_at", -1).to_list(length=None)

            reports = []

            for rep in reports_raw:
                user = None
                owner_id = rep.get("owner_id")

                if owner_id:
                    try:
                        user = await db.user.find_one({
                            "_id": ObjectId(owner_id)
                        })
                    except Exception:
                        user = None

                reports.append({
                    "report_id": str(rep["_id"]),
                    "reporter_id": owner_id,
                    "reporter_username": user["username"] if user else "Unknown",
                    "reporter_email": user["email"] if user else None,
                    "description": rep["description"],
                    "created_at": rep.get("created_at")
                })

            return reports

        except Exception as e:
            logger.error("get_reports_by_article error: %s", e)
            return None

    @staticmethod
    async def delete_reports_by_owner(owner_id: str):
        try:
            reports = await db.report_article.find({
                "owner_id": owner_id
            }).to_list(length=None)

            article_report_count = {}

            for rep in reports:
                article_id = rep.get("article_id")
                if article_id:
                    article_report_count[article_id] = article_report_count.get(article_id, 0) + 1

            await db.report_article.delete_many({
                "owner_id": owner_id
            })

            for article_id, count in article_report_count.items():
                await db.article.update_one(
                    {"_id": article_id},
                    {"$inc": {"report_count": -count}}
                )

            return True

        except Exception as e:
            logger.error("delete_reports_by_owner error: %s", e)
            return False