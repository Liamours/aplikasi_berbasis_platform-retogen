import os
import logging
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from core.limiter import limiter
from core.api_handlers import validation_exception_handler
from routes import auth, article, comment, rating, report_article, report_user, user, subscription, notification
from monitor.router import router as monitor_router
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Updated Backend Template")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000"
).split(",")

logger.info(f"Allowed Origins: {ALLOWED_ORIGINS}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(article.router, prefix="/article", tags=["Article"])
app.include_router(comment.router, prefix="/comment", tags=["Comment"])
app.include_router(rating.router, prefix="/rating", tags=["Rating"])
app.include_router(report_article.router, prefix="/report_article", tags=["Report Article"])
app.include_router(report_user.router, prefix="/report_user", tags=["Report User"])
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(subscription.router, prefix="/subscription", tags=["Subscription"])
app.include_router(notification.router, prefix="/notification", tags=["Notification"])
app.include_router(monitor_router, prefix="/monitor", tags=["Monitor Harga"])

@app.get("/")
def root():
    return {"message": "API Ready"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)