from starlette.datastructures import MutableHeaders
from starlette.requests import cookie_parser
from starlette.types import ASGIApp, Receive, Scope, Send

from src.server.core.security import jwt_encode, jwt_decode


class SessionMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):
            return await self.app(scope, receive, send)

        headers = MutableHeaders(scope=scope)
        cookies = headers.get("cookies", None)

        if cookies is None:
            return  # TODO: create new jwt

        cookies = cookie_parser(cookies)
        jwt = cookies.get("jwt", None)

        if jwt is None:
            return  # TODO: create

        # TODO: else we decode jwt
