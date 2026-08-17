from pydantic import BaseModel


class PostponedResponse(BaseModel):
    id: str
    text: str | None
    media_path: str | None
    group_domain: str
    created_at: str
