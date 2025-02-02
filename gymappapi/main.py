from contextlib import asynccontextmanager

from fastapi import FastAPI

from gymappapi.database import database
from gymappapi.routers import membership


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(membership.router)
