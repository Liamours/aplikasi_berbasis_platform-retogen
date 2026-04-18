from fastapi import APIRouter, HTTPException, Depends, Request

from monitor.schemas import MonitorSearchRequest, MonitorSearchResponse
from monitor.scraper import scrape_tokopedia
from core.dependencies import get_current_user
from core.limiter import limiter

router = APIRouter()


@router.post("/search", response_model=MonitorSearchResponse)
@limiter.limit("20/minute")
def monitor_search(request: Request, body: MonitorSearchRequest, payload: dict = Depends(get_current_user)):
    """
    Search Tokopedia for a product and return top listings with price + rating.
    Requires valid JWT.
    """
    if not body.product_name.strip():
        raise HTTPException(status_code=400, detail="product_name required")

    result = scrape_tokopedia(body.product_name.strip(), limit=body.limit)
    return result


@router.get("/health")
def monitor_health():
    return {"status": "ok"}
