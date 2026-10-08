from uuid import UUID

from pydantic import BaseModel


class TGChannel(BaseModel):
    name: str
    photo_url: str | None


class TGPost(BaseModel):
    reactions: int
    reposts: int
    views: int

    timestamp: int
    is_pinned: bool
    text: str

    photos_url: list[str] | None
