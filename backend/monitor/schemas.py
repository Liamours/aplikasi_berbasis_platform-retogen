from pydantic import BaseModel, Field
from typing import List, Optional


class MonitorSearchRequest(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=200)
    limit: int = Field(default=10, ge=1, le=50)
    min_score: float = Field(default=0.3, ge=0.0, le=1.0, description="Fuzzy relevance threshold (0=no filter, 1=exact). Results below this score are excluded.")


class ProductResult(BaseModel):
    product: str
    store: Optional[str]
    price: Optional[int]
    rating: Optional[float]
    relevance_score: Optional[float] = None


class MonitorSearchResponse(BaseModel):
    results: List[ProductResult]
    errors: List[str]
    total: int
