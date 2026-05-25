from fastapi import APIRouter, Depends
from services.notification_service import NotificationService
from schemas.notification_schema import RegisterFcmTokenRequest, MarkReadRequest
from db.connection import db
from core.dependencies import get_current_user

router = APIRouter()


@router.post("/get")
async def get_notifications(payload: dict = Depends(get_current_user)):
    user = await db.user.find_one({"email": payload.get("email")})
    if not user:
        return {"confirmation": "token invalid"}
    notifications = await NotificationService.get_notifications(str(user["_id"]))
    return {"confirmation": "successful", "notifications": notifications}


@router.post("/register_token")
async def register_fcm_token(req: RegisterFcmTokenRequest, payload: dict = Depends(get_current_user)):
    """Register or update FCM device token for push notifications."""
    user = await db.user.find_one({"email": payload.get("email")})
    if not user:
        return {"confirmation": "token invalid"}
    if not req.fcm_token or not req.fcm_token.strip():
        return {"confirmation": "invalid token"}
    await db.user.update_one(
        {"_id": user["_id"]},
        {"$set": {"fcm_token": req.fcm_token.strip()}}
    )
    return {"confirmation": "successful: token registered"}


@router.post("/mark_read")
async def mark_notification_read(req: MarkReadRequest, payload: dict = Depends(get_current_user)):
    """Mark a single notification as read."""
    user = await db.user.find_one({"email": payload.get("email")})
    if not user:
        return {"confirmation": "token invalid"}
    ok = await NotificationService.mark_read(req.notification_id, str(user["_id"]))
    if not ok:
        return {"confirmation": "not found or already read"}
    return {"confirmation": "successful: marked as read"}


@router.post("/mark_all_read")
async def mark_all_notifications_read(payload: dict = Depends(get_current_user)):
    """Mark all unread notifications as read."""
    user = await db.user.find_one({"email": payload.get("email")})
    if not user:
        return {"confirmation": "token invalid"}
    count = await NotificationService.mark_all_read(str(user["_id"]))
    return {"confirmation": "successful", "marked_count": count}
