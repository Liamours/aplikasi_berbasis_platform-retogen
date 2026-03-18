from pydantic import BaseModel

class AddArticle(BaseModel):
    article_title: str
    article_preview: str
    article_content: str
    article_tag: str
    article_image: str
