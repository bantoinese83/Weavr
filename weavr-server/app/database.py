from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.config import settings

# Create the async engine
engine = create_async_engine(settings.DATABASE_URL, poolclass=NullPool)
test_engine = create_async_engine(settings.TEST_DATABASE_URL, poolclass=NullPool)

# Create the sessionmaker for async sessions
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
TestSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False)


async def get_db():
    async with async_session() as session:
        yield session


async def override_get_db():
    async with TestSessionLocal() as session:
        yield session
