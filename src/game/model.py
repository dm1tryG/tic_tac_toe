from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import SQLModel, Field, create_engine
from typing import Optional


class Game(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: Optional[str] = Field(default=None, nullable=True)
    winner: Optional[str] = Field(default=None, nullable=True)
    board: Optional[str] = Field(default=None, nullable=True)


class Database:
    def __init__(self):
        # TODO: move connection string to Settings Pydantic
        self.engine = AsyncEngine(create_engine(url="sqlite+aiosqlite:///games.db", echo=True, future=True))

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)


# TODO: move to settings
# TODO: move to another container with migrations
engine = create_engine("sqlite:///games.db")
SQLModel.metadata.create_all(engine)
