from fastapi import APIRouter

from .health.endpoints import router as health_router
from .user.endpoints import router as users_router
from .oauth.endpoints import router as oauth_router

router = APIRouter(prefix='/v1')
router.include_router(health_router)
router.include_router(users_router)
router.include_router(oauth_router)
