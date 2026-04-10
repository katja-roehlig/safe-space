from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine, Base, get_db
from models import Exercise, User, UserProperty
from sqlalchemy import select
from auth_utils import (
    hash_password,
    login_check,
    create_access_token,
    decode_acces_token,
)
from schemas import (
    ExerciseCreate,
    ExerciseRead,
    UserCreate,
    UserPropertyOnborading,
    UserRead,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Alles hier drin passiert beim START der App
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Alles nach dem yield passiert beim STOPPEN (optional)


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite / CRA
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# token wird aus dem header gefischt und entschlüsselt, bis wieder die user_id als string dasteht
# jetzt wird geguckt, ob dieser user noch existiert in der User table
async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    user_id = decode_acces_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Ungültiges Token"
        )
    query = select(User).where(User.id == int(user_id))
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User existiert nicht mehr"
        )
    return user


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
async def login_user(
    user_log: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    # zuerst wird nur die abfrage geschrieben (sql) mehr nicht
    query = select(User).where(User.mail == user_log.username)
    # hier wird jetzt wirklich gesucht
    result = await db.execute(query)
    # und jetzt die Ergebnisse bestimmt
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="Falsche Daten")

    if not login_check(str(user.hashed_password), user_log.password):
        raise HTTPException(status_code=400, detail="Falsche Daten")
    user_info = {"sub": str(user.id)}
    token = create_access_token(user_info)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/users/Profile", response_model=UserRead)
async def show_user_profile(current_user: User = Depends(get_current_user)):
    return current_user


@app.post("onboarding")
async def get_onboarding_data(
    onboarding_data: UserPropertyOnborading,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    for item in onboarding_data.strengths:
        user_strength = UserProperty(
            user_id=current_user.id, category="strength", content=item
        )
        db.add(user_strength)
    user_place = UserProperty(
        user_id=current_user.id,
        category="safe_place",
        content=onboarding_data.safe_place,
    )
    db.add(user_place)
    await db.commit()
    return {"message": "Alles gespeichert!"}
