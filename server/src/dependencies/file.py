import os
from pathlib import Path

import aiofiles
from fastapi import UploadFile

from src.core.exceptions import ContentTooLarge, UnsupportedMediaType
from src.core.constants import MediaType
from src.core.config import settings
from src.core.utilities import utc_now
from src.schemas.file import ReadFile


class FileValidator:
    ALLOWED_SIZE = 1024 * 1024 * 10
    CHUNK_BYTES = 1024 * 1024

    async def __call__(self, file: UploadFile) -> ReadFile:
        return await self.validate_file(file)

    def _generate_filename(self, format: str) -> Path:
        return Path(settings.WHERE_TO_STORE_MEDIA / (utc_now().isoformat() + "." + format))

    def _cleanup(self, path: Path) -> None:
        os.remove(path)

    async def validate_file(self, file: UploadFile) -> ReadFile:
        if file.content_type is None:
            raise UnsupportedMediaType("File not allowed with empty content type")

        content_type = file.content_type.split("/")

        try:
            type = MediaType(content_type[0])
        except ValueError:
            raise UnsupportedMediaType("File not allowed with this type")

        filename = self._generate_filename(content_type[1])
        size = 0
        async with aiofiles.open(filename, "wb") as buffer:
            while chunk := await file.read(self.CHUNK_BYTES):
                size += len(chunk)
                if size > self.ALLOWED_SIZE:
                    break
                _ = await buffer.write(chunk)

        if size > self.ALLOWED_SIZE:
            self._cleanup(filename)
            raise ContentTooLarge("File exceeded limit of 10MiB")

        return ReadFile(
            path=filename,
            size=size,
            type=type,
            extension=content_type[1]
        )
