from pydantic import BaseModel


class VKPost(BaseModel):
    likes: int           # response["items"][...]["likes"]["count"]
    reposts: int         # response["items"][...]["resposts"]["count"]
    views: int           # response["items"][...]["views"]["count"]

    timestamp: int       # response["items"][...]["date"]
    is_pinned: bool      # response["items"][...]["is_pinned"]
    text: str            # response["items"][...]["text"]

    # response["items"][...]["attachments"][...]["photo"]["orig_photo"]["url"]
    photos_url: list[str] | None 
