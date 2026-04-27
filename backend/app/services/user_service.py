from fastapi import HTTPException
from sqlalchemy import or_, select
from app.models.models import UserProperty, User


class UserService:
    async def register_user(self, db, new_user):
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

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

    async def user_exists_in_user_properties(self, db, user_id):
        query = select(UserProperty).where(User.id == user_id).limit(1)
        result = await db.execute(query)
        user_exist = result.scalar_one_or_none()
        if user_exist:
            return False
        else:
            return True

    async def save_onboarding_data(self, db, onboarding_data, user):
        query = select(User).where(User.id == int(user.id))
        result = await db.execute(query)
        update_user = result.scalar_one_or_none()
        if not update_user:
            raise HTTPException(status_code=404, detail="User not found")
        update_user.age = onboarding_data.age
        update_user.gender = onboarding_data.gender
        for item in onboarding_data.strengths:
            user_strength = UserProperty(
                user_id=user.id, category="strength", content=item
            )
            db.add(user_strength)
        user_place = UserProperty(
            user_id=user.id,
            category="safe_place",
            content=onboarding_data.safe_place,
        )
        db.add(user_place)
        await db.commit()
        return {"message": "Onboarding successfully completed!", "status": "success"}


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
