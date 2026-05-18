from fastapi import HTTPException
from sqlalchemy import or_, select
from app.models.models import UserProperty, User
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.services.vector_service import VECTOR_SERVICE
from app.core.onboarding_utils import save_safe_place, save_strengths, update_user

logger = logging.getLogger(__name__)


class UserService:
    async def register_user(self, db, new_user):
        db.add(new_user)
        try:
            await db.commit()
            await db.refresh(new_user)
            return new_user
        except SQLAlchemyError as e:
            raise e

    async def login_user(self, db, user_mail):
        query = select(User).where(User.mail == user_mail)
        # hier wird jetzt wirklich gesucht
        result = await db.execute(query)
        # und jetzt die Ergebnisse bestimmt
        user = result.scalar_one_or_none()
        return user

    async def get_one_user(self, db, user_id):
        query = select(User).where(User.id == int(user_id))
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        return user

    async def save_onboarding_data(self, db, onboarding_data, user):
        try:
            await save_strengths(db, onboarding_data, user)
            await save_safe_place(db, onboarding_data, user)
            await update_user(db, onboarding_data, user)
            await db.commit()
            return {
                "message": "Onboarding successfully completed!",
                "status": "success",
            }
        except HTTPException as http_exc:
            for item in db.new:
                if isinstance(item, UserProperty):
                    logger.warning(
                        f"Onboarding error: Deleting vector memory for ID {item.id}."
                    )
                    await VECTOR_SERVICE.delete_memory(str(item.id))
            await db.rollback()
            raise http_exc  # Fehlermeldung ans Frontend weitergeben

        except Exception as e:
            logger.exception(f"Unexpected system error during onboarding: {e}")
            for item in db.new:
                if isinstance(item, UserProperty):
                    await VECTOR_SERVICE.delete_memory(str(item.id))
            await db.rollback()
            raise HTTPException(  # Fehlermeldung an user
                status_code=400,
                detail="An unexpected database error occurred. Please try again.",
            )


class UserPropertyService:
    async def get_user_resources(self, db, user_id):
        query = select(UserProperty).where(
            UserProperty.user_id == user_id,
            or_(
                UserProperty.category == "strength",
                UserProperty.category == "safe_place",
            ),
        )
        result = await db.execute(query)
        elements = result.scalars().all()
        user_strengths = [
            element.content for element in elements if element.category == "strength"
        ]
        user_safe_place = [
            element.content for element in elements if element.category == "safe_place"
        ]
        return user_strengths, user_safe_place
