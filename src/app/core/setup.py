from collections.abc import Callable
from typing import Any
from contextlib import _AsyncGeneratorContextManager, asynccontextmanager

from .config import Settings

from fastapi import FastAPI, APIRouter

@asynccontextmanager
async def _lifespan(api: FastAPI):
    yield

def create_application(
        router: APIRouter,
        settings: Settings,
        lifespan: Callable[[FastAPI], _AsyncGeneratorContextManager[Any]] | None = None,
    ) -> FastAPI:

    if lifespan is None:
        lifespan = _lifespan

    application = FastAPI(lifespan=lifespan, title=settings.PROJECT_NAME, debug=settings.DEBUG)
    application.include_router(router)

    return application
