import logging
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from core.exceptions import Unauthorized
from core.security import JWT_SECRET, JWT_ALGO

logger = logging.getLogger(__name__)
oauth = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        return payload
    except ExpiredSignatureError:
        logger.warning("[AUTH] Rejected expired token")
        raise Unauthorized("Token has expired")
    except InvalidTokenError:
        logger.warning("[AUTH] Rejected invalid token")
        raise Unauthorized("Invalid token")
