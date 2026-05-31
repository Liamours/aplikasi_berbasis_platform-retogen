from pydantic import BaseModel, EmailStr, Field

class ReportUserRequest(BaseModel):
    reported_user_email: EmailStr
    description: str = Field(..., min_length=1, max_length=2048)
