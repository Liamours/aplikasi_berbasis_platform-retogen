from fastapi import APIRouter, Depends
from schemas.subscription_schema import SubscribeRequest, UnsubscribeRequest
from services.subscription_service import SubscriptionService
from db.connection import db
from core.dependencies import get_current_user

router = APIRouter()


async def _resolve_user_id(payload: dict) -> str | None:
    user = await db.user.find_one({"email": payload.get("email")})
    return str(user["_id"]) if user else None


@router.post("/subscribe")
async def subscribe(req: SubscribeRequest, payload: dict = Depends(get_current_user)):
    user_id = await _resolve_user_id(payload)
    if not user_id:
        return {"confirmation": "token invalid"}
    tag = req.tag.strip().lower()
    if not tag:
        return {"confirmation": "tag cannot be empty"}
    result = await SubscriptionService.subscribe(user_id, tag)
    if result == "error":
        return {"confirmation": "backend error"}
    return {"confirmation": result}


@router.post("/unsubscribe")
async def unsubscribe(req: UnsubscribeRequest, payload: dict = Depends(get_current_user)):
    user_id = await _resolve_user_id(payload)
    if not user_id:
        return {"confirmation": "token invalid"}
    tag = req.tag.strip().lower()
    if not tag:
        return {"confirmation": "tag cannot be empty"}
    result = await SubscriptionService.unsubscribe(user_id, tag)
    if result == "error":
        return {"confirmation": "backend error"}
    return {"confirmation": result}


@router.post("/get")
async def get_subscriptions(payload: dict = Depends(get_current_user)):
    user_id = await _resolve_user_id(payload)
    if not user_id:
        return {"confirmation": "token invalid"}
    tags = await SubscriptionService.get_subscriptions(user_id)
    return {"confirmation": "successful", "tags": tags}
