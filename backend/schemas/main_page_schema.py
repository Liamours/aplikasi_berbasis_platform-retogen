from pydantic import BaseModel
from typing import Optional
from enum import Enum

class SortOption(str, Enum):
    newest = "newest"
    oldest = "oldest"
    most_reported = "most_reported"
    by_tag = "by_tag"
    search_title = "search_title"
    highest_rated = "highest_rated"
    most_commented = "most_commented"

class MainPageRequest(BaseModel):
    sort: Optional[SortOption] = SortOption.newest
    tag: Optional[str] = None
    search: Optional[str] = None
