from pathlib import Path

from pydantic import BaseModel

from src.core.constants import MediaType


class ReadFile(BaseModel):
    path: Path
    size: int
    type: MediaType
    extension: str
