from fastapi import APIRouter, Depends
from schemas.edit_article_get_schema import EditArticleGetRequest
from schemas.edit_article_update_schema import EditArticleUpdateRequest
from schemas.view_article_schema import ViewArticleRequest
from services.article_service import ArticleService
from services.auth_service import AuthService
from services.subscription_service import SubscriptionService
from services.notification_service import NotificationService
from services.article_view import build_article_view
from utils.base64_utils import base64_to_bytes, bytes_to_base64
from utils.image_validator import validate_image_bytes
from schemas.delete_article_schema import DeleteArticleRequest
from schemas.add_article_schema import AddArticle
from schemas.main_page_schema import MainPageRequest
from core.dependencies import get_current_user, get_current_user_doc

router = APIRouter()


def _validate_article_fields(req) -> str | None:
    """Returns error message if invalid, None if OK."""
    if not req.article_title or not (1 <= len(req.article_title) <= 256):
        return "Title must be 1-256 characters long."
    if not req.article_preview or not (1 <= len(req.article_preview) <= 128):
        return "Preview must be 1-128 characters long."
    if not req.article_content or not (1 <= len(req.article_content) <= 65536):
        return "Content must be 1-65536 characters long."
    return None


@router.post("/edit/get")
async def edit_get_article(req: EditArticleGetRequest, payload: dict = Depends(get_current_user)):
    if not AuthService.is_admin(payload):
        return {"confirmation": "not admin"}

    article = await ArticleService.fetch_article(req.article_id)
    if article is None:
        return {"confirmation": "backend error"}

    image_base64 = None
    if article.get("article_image"):
        image_base64 = bytes_to_base64(bytes(article["article_image"]))

    return {
        "confirmation": "successful",
        "article_id": str(article["_id"]),
        "article_title": article["article_title"],
        "article_preview": article["article_preview"],
        "article_content": article["article_content"],
        "article_tags": article.get("article_tags", []),
        "article_image": image_base64,
        "product_name": article.get("product_name")
    }


@router.post("/edit/update")
async def edit_update_article(req: EditArticleUpdateRequest, payload: dict = Depends(get_current_user)):
    if not AuthService.is_admin(payload):
        return {"confirmation": "not admin"}

    article = await ArticleService.fetch_article(req.article_id)
    if article is None:
        return {"confirmation": "backend error"}

    err = _validate_article_fields(req)
    if err:
        return {"confirmation": err}

    try:
        image_bytes = base64_to_bytes(req.article_image) if req.article_image else None
    except Exception:
        return {"confirmation": "invalid image format"}

    result = await ArticleService.update_article(req, image_bytes)

    if result == "invalid_image":
        return {"confirmation": "invalid image format"}
    if not result:
        return {"confirmation": "backend error"}

    return {"confirmation": "successful: article edited", "article_id": req.article_id}


@router.post("/view")
async def view_article(req: ViewArticleRequest, payload: dict = Depends(get_current_user)):
    article = await ArticleService.fetch_article(req.article_id)
    if article is None:
        return {"confirmation": "backend error"}
    return await build_article_view(article, payload)


@router.post("/delete")
async def delete_article(req: DeleteArticleRequest, payload: dict = Depends(get_current_user)):
    if not AuthService.is_admin(payload):
        return {"confirmation": "not admin"}

    article = await ArticleService.fetch_article(req.article_id)
    if article is None:
        return {"confirmation": "backend error"}

    deleted = await ArticleService.soft_delete(req.article_id)
    if not deleted:
        return {"confirmation": "backend error"}

    return {"confirmation": "successful: article deleted"}


@router.post("/main_page")
async def main_page(req: MainPageRequest, payload: dict = Depends(get_current_user), user=Depends(get_current_user_doc)):
    if not user:
        return {"confirmation": "token invalid"}

    user_email = payload.get("email")

    articles = await ArticleService.get_articles_filtered(
        sort=req.sort.value,
        tag=req.tag,
        search=req.search
    )

    if articles is None:
        return {"confirmation": "backend error"}

    list_article = []
    for a in articles:
        image = None
        if a.get("article_image"):
            try:
                image = bytes_to_base64(bytes(a["article_image"]))
            except Exception:
                image = None
        list_article.append({
            "article_id": str(a["_id"]),
            "article_title": a.get("article_title"),
            "article_preview": a.get("article_preview"),
            "article_tags": a.get("article_tags", []),
            "article_image": image
        })

    return {
        "confirmation": "fetch data successful",
        "username": user.get("username", ""),
        "sort": req.sort.value,
        "tag": req.tag,
        "search": req.search,
        "list_article": list_article
    }


@router.post("/verification")
async def verification(payload: dict = Depends(get_current_user)):
    if not AuthService.is_admin(payload):
        return {"confirmation": "not admin"}
    return {"confirmation": "successful"}


@router.post("/add")
async def add_article(req: AddArticle, payload: dict = Depends(get_current_user), user=Depends(get_current_user_doc)):
    if not AuthService.is_admin(payload):
        return {"confirmation": "not admin"}

    if not user:
        return {"confirmation": "token invalid"}

    author_id = str(user["_id"])

    err = _validate_article_fields(req)
    if err:
        return {"confirmation": err}
    if not req.article_tags:
        return {"confirmation": "At least one tag is required."}

    try:
        image_bytes = base64_to_bytes(req.article_image)
    except Exception:
        return {"confirmation": "Image format must be valid Base64."}

    if not validate_image_bytes(image_bytes):
        return {"confirmation": "invalid image format"}

    normalized_tags = [t.strip().lower() for t in req.article_tags]

    article_id = await ArticleService.add_article(
        req.article_title,
        req.article_preview,
        req.article_content,
        normalized_tags,
        image_bytes,
        author_id,
        product_name=req.product_name
    )

    if article_id is None:
        return {"confirmation": "backend error"}

    subscriber_ids = await SubscriptionService.get_subscribers_for_tags(normalized_tags)
    subscriber_ids = [uid for uid in subscriber_ids if uid != author_id]
    await NotificationService.create_notifications(
        subscriber_ids, article_id, req.article_title, normalized_tags
    )

    return {"confirmation": "success: article added"}
