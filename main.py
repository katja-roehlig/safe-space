from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine, Base, get_db
from models import Exercise, User
from sqlalchemy import select
from auth_utils import hash_password, login_check
from schemas import ExerciseCreate, ExerciseRead, UserCreate, UserLogin, UserRead


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


@app.post("/register", response_model=UserRead)
async def register_user(user_reg: UserCreate, db: AsyncSession = Depends(get_db)):
    # passwort verschlüsseln
    hashed_pwd = hash_password(user_reg.password)

    # neuen user anlegen
    new_user = User(
        mail=user_reg.mail, nickname=user_reg.nickname, hashed_password=hashed_pwd
    )
    # zur table user hinzufügen

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@app.post("/login")
async def login_user(user_log: UserLogin, db: AsyncSession = Depends(get_db)):
    # zuerst wird nur die abfrage geschrieben (sql) mehr nicht
    query = select(User).where(User.mail == user_log.mail)
    # hier wird jetzt wirklich gesucht
    result = await db.execute(query)
    # und jetzt die Ergebnisse bestimmt
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="Falsche Daten")

    if login_check(str(user.hashed_password), user_log.password):
        return {"message": "Login erfolgreich"}
