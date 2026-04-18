from fastapi import APIRouter, Request
from schemas.login_schema import LoginUser
from schemas.register_schema import RegisterUser
from services.auth_service import AuthService
from core.limiter import limiter
import re

router = APIRouter()

def validate_register_input(data: RegisterUser):
    if not re.fullmatch(r"^[A-Za-z0-9]{8,16}$", data.username):
        return {"confirmation": "username length must be 8 - 16 characters, only alphabetic characters and numbers (aA-zZ, 0-9) are allowed"}
    if not re.fullmatch(r"^[A-Za-zA-Z ]{4,32}$", data.fullname):
        return {"confirmation": "fullname length must be 4 - 32 characters, only alphabetic characters and spaces are allowed"}
    password = data.password
    if len(password) < 8 or len(password) > 16:
        return {"confirmation": "password length must be 8 - 16 characters"}
    if not re.search(r"[a-z]", password):
        return {"confirmation": "password must contain at least one lowercase letter"}
    if not re.search(r"[A-Z]", password):
        return {"confirmation": "password must contain at least one uppercase letter"}
    if not re.search(r"\d", password):
        return {"confirmation": "password must contain at least one number"}
    if not password.isalnum():
        return {"confirmation": "password can only contain letters and numbers"}
    return None

def validate_login_input(data: LoginUser):
    if not data.email:
        return {"confirmation": "email doesn't exist"}
    if not data.password:
        return {"confirmation": "password is incorrect"}
    return None

@router.post("/registration")
@limiter.limit("5/minute")
async def register(request: Request, data: RegisterUser):
    validate_error = validate_register_input(data)
    if validate_error:
        return validate_error
    return await AuthService.register(data)

@router.post("/login")
@limiter.limit("10/minute")
async def login(request: Request, data: LoginUser):
    validate_error = validate_login_input(data)
    if validate_error:
        return validate_error
    return await AuthService.login(data)
