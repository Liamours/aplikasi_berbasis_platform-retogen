from fastapi import APIRouter, Depends
from services.notification_service import NotificationService
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
