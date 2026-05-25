from pydantic import BaseModel


class RegisterFcmTokenRequest(BaseModel):
    fcm_token: str


class MarkReadRequest(BaseModel):
    notification_id: str
