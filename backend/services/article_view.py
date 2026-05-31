import logging
from bson import ObjectId
from db.connection import db
from services.comment_service import CommentService
from services.rating_service import RatingService
from services.report_article_service import ReportArticleService
from services.auth_service import AuthService
from utils.base64_utils import bytes_to_base64

logger = logging.getLogger(__name__)


async def build_article_view(article: dict, payload: dict) -> dict:
    """
    Build full article view response shared by /article/view, /comment/*, /rating/*.
    Batches all user lookups into a single $in query — no N+1.
    """
    article_id = str(article["_id"])
    user_email = payload.get("email")
    is_admin = AuthService.is_admin(payload)

    user = await db.user.find_one({"email": user_email})

    image_base64 = None
    if article.get("article_image"):
        try:
            image_base64 = bytes_to_base64(bytes(article["article_image"]))
        except Exception as e:
            logger.warning("Image decode failed for article %s: %s", article_id, e)

    comments_raw = await CommentService.get_comments(article_id) or []
    ratings_raw = await RatingService.get_ratings(article_id) or []

    # Batch-fetch all owner users in one query
    owner_ids = set()
    for c in comments_raw:
        if c.get("owner_id"):
            owner_ids.add(c["owner_id"])
    for r in ratings_raw:
        if r.get("owner_id"):
            owner_ids.add(r["owner_id"])

    users_by_id = {}
    if owner_ids:
        oid_list = []
        for oid in owner_ids:
            try:
                oid_list.append(ObjectId(oid))
            except Exception:
                logger.debug("Skipping malformed owner_id: %r", oid)
        if oid_list:
            async for u in db.user.find({"_id": {"$in": oid_list}}, {"username": 1, "email": 1}):
                users_by_id[str(u["_id"])] = u

    comments = [
        {
            "comment_id": str(c["_id"]),
            "parent_comment_id": c.get("parent_comment_id"),
            "owner": users_by_id.get(str(c["owner_id"]), {}).get("username", "Unknown"),
            "user_email": users_by_id.get(str(c["owner_id"]), {}).get("email"),
            "comment_content": c["comment_content"],
        }
        for c in comments_raw
    ]

    ratings = [
        {
            "rating_id": str(r["_id"]),
            "owner": users_by_id.get(str(r["owner_id"]), {}).get("username", "Unknown"),
            "user_email": users_by_id.get(str(r["owner_id"]), {}).get("email"),
            "rating_value": r["rating_value"],
        }
        for r in ratings_raw
    ]

    response = {
        "confirmation": "successful",
        "userclass": "admin" if is_admin else "user",
        "user_email": user_email,
        "username": user["username"] if user else "Unknown",
        "article_title": article["article_title"],
        "article_content": article["article_content"],
        "article_tags": article.get("article_tags", []),
        "article_image": image_base64,
        "product_name": article.get("product_name"),
        "comments": comments,
        "ratings": ratings,
    }

    if is_admin:
        reports = await ReportArticleService.get_reports_by_article(article_id)
        response["report_count"] = article.get("report_count", 0)
        response["reports"] = reports or []

    return response
