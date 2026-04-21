from pydantic import BaseModel, EmailStr


# diese schemas werden auch oft dto (DataTransferObjekt) oder pojo genannt
# gibt der user beim erstellen(POST) ein
class ExerciseCreate(BaseModel):
    title: str
    content: str
    category: str


# wird mitgeschickt, wenn das FE die daten abruft
class ExerciseRead(ExerciseCreate):
    id: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    mail: EmailStr
    password: str
    nickname: str


class UserRead(BaseModel):
    id: int
    mail: EmailStr
    nickname: str

    class Config:
        from_attributes = True


class ReturnedLoginData(BaseModel):
    access_token: str
    token_type: str
    has_onboarding: bool
    nickname: str


class UserOnboarding(BaseModel):
    age: int
    gender: str
    strengths: list[str]
    safe_place: str


class ChatItem(BaseModel):
    id: str
    role: str
    content: str


# class ChatContent(BaseModel):
#     conversations: list[ChatItem]
