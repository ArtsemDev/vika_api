from inspect import iscoroutinefunction
from typing import Type, Any, Sequence

from pydantic import BaseModel
from sqlalchemy import Column, INT, create_engine, Row, RowMapping
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker, declared_attr


class Base(DeclarativeBase):
    id = Column(INT, primary_key=True)

    engine = create_engine('postgresql://dev:F6r58h7G2e@127.0.0.1:5432/fastapi')
    session = sessionmaker(bind=engine)

    async_engine = create_async_engine('postgresql+asyncpg://dev:F6r58h7G2e@127.0.0.1:5432/fastapi')
    async_session = async_sessionmaker(bind=async_engine)

    @staticmethod
    def create_session(func):
        def wrapper(*args, **kwargs):
            with Base.session() as session:
                return func(*args, **kwargs, session=session)

        async def async_wrapper(*args, **kwargs):
            async with Base.async_session() as session:
                return await func(*args, **kwargs, session=session)

        return async_wrapper if iscoroutinefunction(func) else wrapper

    @declared_attr
    def __tablename__(cls) -> str:
        return ''.join(f'_{i.lower()}' if i.isupper() else i for i in cls.__name__).strip('_')

    @create_session
    async def save(self, session: AsyncSession = None) -> None:
        session.add(self)
        await session.commit()
        await session.refresh(self)

    @classmethod
    @create_session
    async def get(cls, pk: Any, session: AsyncSession = None) -> Type["Base"]:
        return await session.get(cls, pk)

    @create_session
    async def delete(self, session: AsyncSession = None) -> None:
        await session.delete(self)
        await session.commit()

    @classmethod
    @create_session
    async def scalars(cls, sql: Any, session: AsyncSession = None) -> Sequence[Row | RowMapping | Any]:
        objs = await session.scalars(sql)
        return objs.all()

    @classmethod
    @create_session
    async def execute(cls, sql: Any, session: AsyncSession = None) -> Sequence[Row | RowMapping | Any]:
        objs = await session.execute(sql)
        return objs.all()

    def from_pydantic(self, schema: BaseModel):
        for key, val in schema.dict(exclude={'id'}).items():
            setattr(self, key, val)

    def dict(self) -> dict:
        data = self.__dict__
        if '_sa_instance_state' in data:
            del data['_sa_instance_state']
        return data
