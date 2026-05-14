import asyncio
from fastapi import APIRouter, HTTPException, Depends, Request

from monitor.schemas import MonitorSearchRequest, MonitorSearchResponse
from monitor.scraper import scrape_tokopedia
from core.dependencies import get_current_user
from core.limiter import limiter

router = APIRouter()


@router.post("/search", response_model=MonitorSearchResponse)
@limiter.limit("20/minute")
async def monitor_search(request: Request, body: MonitorSearchRequest, payload: dict = Depends(get_current_user)):
    """
    Search Tokopedia for a product and return top listings with price + rating.
    Requires valid JWT.
    """
    if not body.product_name.strip():
        raise HTTPException(status_code=400, detail="product_name required")

    # Run blocking scraper in thread pool — avoids blocking the async event loop
    result = await asyncio.to_thread(
        scrape_tokopedia,
        body.product_name.strip(),
        body.limit,
        body.min_score,
    )
    return result


@router.get("/health")
async def monitor_health():
    return {"status": "ok"}
