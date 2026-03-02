from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .models import Base, User, PersonalWord
from config import DATABASE_URL
from sqlalchemy import select, update

engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_or_create_user(user_id, username=None):
    async with SessionLocal() as session:
        user = await session.get(User, user_id)
        if not user:
            user = User(id=user_id, username=username)
            session.add(user)
            await session.commit()
        return user
