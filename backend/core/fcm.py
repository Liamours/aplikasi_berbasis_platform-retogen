import json
import logging
import os
import threading

logger = logging.getLogger(__name__)

_initialized = False
_init_lock = threading.Lock()


def _init_firebase():
    global _initialized
    if _initialized:
        return True
    with _init_lock:
        if _initialized:   # re-check inside lock
            return True
    try:
        import firebase_admin
        from firebase_admin import credentials

        cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
        cred_json = os.getenv("FIREBASE_CREDENTIALS_JSON")

        if cred_path and os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
        elif cred_json:
            cred = credentials.Certificate(json.loads(cred_json))
        else:
            logger.warning("FCM: No Firebase credentials found. Push notifications disabled.")
            return False

        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)

        _initialized = True
        logger.info("FCM: Firebase Admin initialized.")
        return True
    except Exception as e:
        logger.error("FCM: Firebase init failed: %s", e)
        return False


async def send_push(token: str, title: str, body: str, data: dict = None) -> bool:
    """Send FCM push to a single device token. Non-blocking via asyncio.to_thread."""
    import asyncio
    return await asyncio.to_thread(_send_push_sync, token, title, body, data or {})


def _send_push_sync(token: str, title: str, body: str, data: dict) -> bool:
    if not _init_firebase():
        return False
    try:
        from firebase_admin import messaging
        msg = messaging.Message(
            notification=messaging.Notification(title=title, body=body or None),
            data={k: str(v) for k, v in data.items()},
            token=token,
        )
        messaging.send(msg)
        return True
    except Exception as e:
        logger.warning("FCM: Push failed for token %s: %s", token[:12], e)
        return False


async def send_push_multicast(tokens: list[str], title: str, body: str, data: dict = None) -> dict:
    """Send FCM to multiple tokens. Returns {success: int, failure: int}."""
    import asyncio
    return await asyncio.to_thread(_send_multicast_sync, tokens, title, body, data or {})


def _send_multicast_sync(tokens: list[str], title: str, body: str, data: dict) -> dict:
    if not tokens or not _init_firebase():
        return {"success": 0, "failure": 0}
    try:
        from firebase_admin import messaging
        msg = messaging.MulticastMessage(
            notification=messaging.Notification(title=title, body=body or None),
            data={k: str(v) for k, v in data.items()},
            tokens=tokens,
        )
        resp = messaging.send_each_for_multicast(msg)
        return {"success": resp.success_count, "failure": resp.failure_count}
    except Exception as e:
        logger.error("FCM: Multicast failed: %s", e)
        return {"success": 0, "failure": len(tokens)}
