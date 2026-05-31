from fastapi import APIRouter, Depends
from schemas.subscription_schema import SubscribeRequest, UnsubscribeRequest
from services.subscription_service import SubscriptionService
from core.dependencies import get_current_user_doc

router = APIRouter()


@router.post("/subscribe")
async def subscribe(req: SubscribeRequest, user=Depends(get_current_user_doc)):
    if not user:
        return {"confirmation": "token invalid"}
    tag = req.tag.strip().lower()
    if not tag:
        return {"confirmation": "tag cannot be empty"}
    result = await SubscriptionService.subscribe(str(user["_id"]), tag)
    if result == "error":
        return {"confirmation": "backend error"}
    return {"confirmation": result}


@router.post("/unsubscribe")
async def unsubscribe(req: UnsubscribeRequest, user=Depends(get_current_user_doc)):
    if not user:
        return {"confirmation": "token invalid"}
    tag = req.tag.strip().lower()
    if not tag:
        return {"confirmation": "tag cannot be empty"}
    result = await SubscriptionService.unsubscribe(str(user["_id"]), tag)
    if result == "error":
        return {"confirmation": "backend error"}
    return {"confirmation": result}


@router.post("/get")
async def get_subscriptions(user=Depends(get_current_user_doc)):
    if not user:
        return {"confirmation": "token invalid"}
    tags = await SubscriptionService.get_subscriptions(str(user["_id"]))
    return {"confirmation": "successful", "tags": tags}
