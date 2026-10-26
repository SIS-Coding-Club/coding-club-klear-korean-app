from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import Base, engine
from . import models
from .auth import router as auth_router
from .module_particle import router as module_particle_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)

app.include_router(module_particle_router)


@app.get("/")
async def home():
    return {"message" : "This is a test homepage"}