from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, String, ForeignKey

from data import URL

engine = create_async_engine(url=URL,
                             echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass
 

class User(Base):
    __tablename__ = 'users'
 
    tg_id = mapped_column(BigInteger, primary_key = True)
    name: Mapped[str] = mapped_column(String(30))
    phone: Mapped[int]


class Date(Base):
    __tablename__ = 'dates'

    id: Mapped[int] = mapped_column(primary_key = True)
    year: Mapped[int]
    month: Mapped[int]


class Time(Base):
    __tablename__ = 'times'

    id: Mapped[int] = mapped_column(primary_key = True)
    hour: Mapped[int]
    minute: Mapped[int]


class Table(Base):
    __tablename__ = 'tables'

    id: Mapped[int] = mapped_column(primary_key = True)
 
 
class Book(Base):
    __tablename__ = 'books'
 
    id: Mapped[int] = mapped_column(primary_key = True)
    date: Mapped[int] = mapped_column(ForeignKey('dates.id'))
    day: Mapped[int]
    time: Mapped[str] = mapped_column(ForeignKey('times.id'))
    table: Mapped[int] = mapped_column(ForeignKey('tables.id'))
    quantity: Mapped[int]
    comment: Mapped[str] = mapped_column(String(125))
    status: Mapped[str] = mapped_column(String(5))
    user_tg: Mapped[int] = mapped_column(ForeignKey('users.tg_id'))


class Image(Base):
    __tablename__ = 'images'

    tg_id: Mapped[str] = mapped_column(primary_key = True)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
