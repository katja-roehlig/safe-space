from pydantic import BaseModel


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
