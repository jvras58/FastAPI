import time

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware


class AuthorizationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)
        # self.auth = auth

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        # print(f'Process time: {process_time}')
        response.headers['X-Process-Time'] = str(process_time)
        return response
