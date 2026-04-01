from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine, Base, get_db
from models import Exercise
from sqlalchemy import select

from schemas import ExerciseCreate, ExerciseRead


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Alles hier drin passiert beim START der App
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Alles nach dem yield passiert beim STOPPEN (optional)


app = FastAPI(lifespan=lifespan)


@app.get("/exercises")
async def show_exercises(db: AsyncSession = Depends(get_db)):
    query = select(Exercise)
    result = await db.execute(query)
    exercises = result.scalars().all()
    return exercises


@app.post("/exercises", response_model=ExerciseRead)
async def add_exercises(user_input: ExerciseCreate, db: AsyncSession = Depends(get_db)):
    new_exercise = Exercise(
        title=user_input.title, content=user_input.content, category=user_input.category
    )
    db.add(new_exercise)
    await db.commit()  # new_exercise wird in die db geschrieben
    await db.refresh(
        new_exercise
    )  # new exercise wird aktualisiert, mit id versehen und dann returnt
    return new_exercise
