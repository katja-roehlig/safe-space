from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from ai_handler import get_ai_response
from database import engine, Base, get_db
from models import Exercise, User
from sqlalchemy import select
from auth_utils import (
    hash_password,
    login_check,
    create_access_token,
    decode_acces_token,
)
from schemas import (
    ChatItem,
    ExerciseCreate,
    ExerciseRead,
    ReturnedLoginData,
    UserCreate,
    UserOnboarding,
    UserRead,
)
from service import UserService


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
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
USER_SERVICE = UserService()


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
    user = await USER_SERVICE.get_one_user(db, user_id)
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
    await USER_SERVICE.register_user(db, new_user)
    return new_user


@app.post("/login", response_model=ReturnedLoginData)
async def login_user(
    user_log: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user = await USER_SERVICE.login_user(db, user_log.username)
    # Achtung: username ist hier das Hauptidentifizierungsmerkmal, egal, ob das Mail, name telefonnumber ist - es heißt immer username!
    if not user:
        raise HTTPException(status_code=400, detail="Falsche Daten")

    if not login_check(str(user.hashed_password), user_log.password):
        raise HTTPException(status_code=400, detail="Falsche Daten")
    has_onboarding = await USER_SERVICE.user_exists_in_user_properties(db, user.id)
    user_info = {"sub": str(user.id)}
    token = create_access_token(user_info)
    return {
        "access_token": token,
        "token_type": "bearer",
        "hasOnboarding": has_onboarding,
        "nickname": user.nickname,
    }


@app.get("/users/Profile", response_model=UserRead)
async def show_user_profile(current_user: User = Depends(get_current_user)):
    return current_user


@app.post("/onboarding")
async def get_onboarding_data(
    onboarding_data: UserOnboarding,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    success_data = await USER_SERVICE.save_onboarding_data(
        db, onboarding_data, current_user
    )
    return success_data


@app.post("/chat")
async def handle_chat(
    conversation: list[ChatItem],
    current_user: User = Depends(get_current_user),
):
    print("ChatData:", conversation)
    response = await get_ai_response(conversation)
    ai_response, input_tokens, chached_tockens, output_tokens = response
    print("Das kommt von der Ai zurück:", response)
    return {"role": "assistant", "content": ai_response}
