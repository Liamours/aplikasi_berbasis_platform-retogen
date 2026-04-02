from pydantic import BaseModel
from typing import Optional, List

class EditArticleUpdateRequest(BaseModel):
    article_id: str
    article_title: Optional[str] = None
    article_preview: Optional[str] = None
    article_content: Optional[str] = None
    article_tags: Optional[List[str]] = None
    article_image: Optional[str] = None
