from pydantic import BaseModel, EmailStr


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


class UserLogin(BaseModel):
    mail: EmailStr
    password: str


class UserPropertyOnborading(BaseModel):
    strengths: list[str]
    safe_place: str


# class UserPropertyCreate(BaseModel):
#     content: str
