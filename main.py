from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import engine, Base
from models import Exercise  # Wichtig, damit Base die Tabellen kennt!


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Alles hier drin passiert beim START der App
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Alles nach dem yield passiert beim STOPPEN (optional)


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"Hello World!"}
