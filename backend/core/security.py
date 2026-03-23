import bcrypt
import jwt
import os
import logging
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)

JWT_SECRET = os.getenv("JWT_SECRET", "default_secret")
if JWT_SECRET == "default_secret":
    logger.warning("JWT_SECRET is not set — using insecure default. Set the JWT_SECRET environment variable.")
JWT_ALGO = os.getenv("JWT_ALGO", "HS256")

def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))

def create_token(data: dict, expires_minutes: int = 60):
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
