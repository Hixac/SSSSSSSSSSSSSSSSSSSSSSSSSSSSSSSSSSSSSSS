from typing import Annotated
from fastapi import APIRouter, Depends

from src.server.core.database import AsyncSession, get_db_session
from src.server.core.exceptions import Unauthorized

from .service import oauth_service
from .schemas import OAuthPasswordSchema


router = APIRouter(prefix="/oauth", tags=["oauth"])


@router.post(
    "/login",
    status_code=200,
    responses={
        200: {"description": "Passed"},
        401: {"description": "Wrong email or password"}
    }
)
async def login(
    oauth: OAuthPasswordSchema,
    session: Annotated[AsyncSession, Depends(get_db_session)]
):
    user = await oauth_service.authenticate(session, email=oauth.email, password=oauth.password)

    if user is None:
        raise Unauthorized("Wrong email or password")
