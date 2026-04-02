from pydantic import BaseModel

class SubscribeRequest(BaseModel):
    tag: str

class UnsubscribeRequest(BaseModel):
    tag: str
