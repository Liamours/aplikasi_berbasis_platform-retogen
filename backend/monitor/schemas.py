from pydantic import BaseModel, Field
from typing import List, Optional


class MonitorSearchRequest(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=200)
    limit: int = Field(default=10, ge=1, le=50)


class ProductResult(BaseModel):
    product: str
    store: Optional[str]
    price: Optional[int]
    rating: Optional[float]


class MonitorSearchResponse(BaseModel):
    results: List[ProductResult]
    errors: List[str]
    total: int
