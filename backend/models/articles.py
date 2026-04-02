from pydantic import BaseModel
from typing import List

class Article(BaseModel):
    article_title: str
    article_preview: str
    article_content: str
    article_tags: List[str]
    article_image: bytes