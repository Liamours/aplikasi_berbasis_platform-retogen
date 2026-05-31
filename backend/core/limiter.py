import os
from slowapi import Limiter
from starlette.requests import Request


def _get_real_ip(request: Request) -> str:
    """
    Extract real client IP respecting Railway / reverse-proxy forwarding.
    Railway injects X-Forwarded-For; fall back to direct connection IP.
    """
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # X-Forwarded-For may be a comma-separated list; first entry is the real client IP
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


limiter = Limiter(key_func=_get_real_ip)
