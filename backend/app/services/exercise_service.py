from sqlalchemy import select
from app.models.models import Exercise
from sqlalchemy.exc import SQLAlchemyError


class ExerciseService:
    async def add_exercise(self, db, exercise):
        db.add(exercise)
        try:
            await db.commit()  # new_exercise wird in die db geschrieben
            await db.refresh(
                exercise
            )  # new exercise wird aktualisiert, mit id versehen und dann returnt
            return exercise
        except SQLAlchemyError as e:
            await db.rollback()
            raise e

    async def get_all_exercises(self, db):
        query = select(Exercise)
        try:
            result = await db.execute(query)
            exercises = result.scalars().all()
            return exercises
        except SQLAlchemyError as e:
            await db.rollback()
            raise e

    async def delete_exercise(self, db, id):
        exercise_to_delete = await db.get(Exercise, id)
        if not exercise_to_delete:
            return None
        await db.delete(exercise_to_delete)
        try:
            await db.commit()
            return id
        except SQLAlchemyError as e:
            await db.rollback()
            return e

    async def update_exercise(self, db, id, update_exercise):
        exercise_to_update = await db.get(Exercise, id)
        if not exercise_to_update:
            return None
        exercise_to_update.title = update_exercise.title
        exercise_to_update.content = update_exercise.content
        exercise_to_update.instructions = update_exercise.instructions
        exercise_to_update.media = update_exercise.media
        try:
            await db.commit()
            return exercise_to_update
        except SQLAlchemyError as e:
            await db.rollback()
            raise e
