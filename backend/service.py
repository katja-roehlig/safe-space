from sqlalchemy import select
from models import User, UserProperty


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
        user_exists = result.scalar_one_or_none()
        if user_exists is None:
            return False
        else:
            return True
