from pydantic import BaseModel, Field
from typing import List, Optional


class MonitorSearchRequest(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=200)
    limit: int = Field(default=10, ge=1, le=50)
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)
    location: Optional[str] = Field(default=None, max_length=120)
    fcity: Optional[str] = Field(default=None, max_length=120, pattern=r"^\d+(,\d+)*$")
    min_score: float = Field(default=0.3, ge=0.0, le=1.0, description="Fuzzy relevance threshold (0=no filter, 1=exact). Results below this score are excluded.")


class ProductResult(BaseModel):
    product: str
    store: Optional[str]
    seller_city: Optional[str] = None
    price: Optional[int]
    rating: Optional[float]
    relevance_score: Optional[float] = None


class MonitorSearchResponse(BaseModel):
    results: List[ProductResult]
    errors: List[str]
    total: int
    detected_city: Optional[str] = None
    applied_location: Optional[str] = None
    location_filter_applied: bool = False
    location_fallback_used: bool = False
