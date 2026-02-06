
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.server.core.exceptions import ManysError


async def manys_exception_handler(
    request: Request, exc: ManysError # pyright: ignore[reportUnusedParameter]
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": type(exc).__name__, "detail": exc.message},
        headers=exc.headers
    )


def add_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        ManysError,
        manys_exception_handler  # pyright: ignore[reportArgumentType]
    )
