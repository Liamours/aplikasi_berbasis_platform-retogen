import logging
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from core.exceptions import Unauthorized
from core.security import JWT_SECRET, JWT_ALGO

logger = logging.getLogger(__name__)

bearer_scheme = HTTPBearer(
    scheme_name="Bearer Token",
    description="Masukkan JWT token saja. Tidak perlu menulis 'Bearer'."
)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        return payload

    except ExpiredSignatureError:
        logger.warning("[AUTH] Rejected expired token")
        raise Unauthorized("Token has expired")

    except InvalidTokenError:
        logger.warning("[AUTH] Rejected invalid token")
        raise Unauthorized("Invalid token")