from contextlib import asynccontextmanager

import logging
from urllib.request import Request

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler

from gymappapi.database import database
from gymappapi.logging import configure_logging
from gymappapi.routers import membership

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.add_middleware(CorrelationIdMiddleware)
app.include_router(membership.router)


@app.exception_handler(HTTPException)
async def http_exception_handler_logging(request: Request, exc: HTTPException):
    logger.error(f'HTTPException: {exc.status_code} {exc.detail}')
    return await http_exception_handler(request, exc)
