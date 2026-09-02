from pydantic import BaseModel


class PostponedResponse(BaseModel):
    id: str
    text: str
    media_path: str
    group_domain: str
    created_at: str
