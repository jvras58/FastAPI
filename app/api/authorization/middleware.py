"""Authorization Middleware Module."""
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.utils.logging import get_logger

logger = get_logger('authorization.middleware')


class AuthorizationMiddleware(BaseHTTPMiddleware):
    """Middleware to handle authorization tasks."""

    def __init__(self, app: ASGIApp):
        super().__init__(app)
        # self.auth = auth

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers['X-Process-Time'] = str(process_time)
        logger.info(
            'Request %s %s -> %s in %.4fs',
            request.method,
            request.url.path,
            response.status_code,
            process_time,
        )
        return response
