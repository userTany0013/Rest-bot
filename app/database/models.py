from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, String, ForeignKey

engine = create_async_engine(url='sqlite+aiosqlite:///database.db',
                             echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass
 

class User(Base):
    tablename = 'users'
 
    tg_id = mapped_column(BigInteger, primary_key = True)
    name: Mapped[str] = mapped_column(String(30))
    phone: Mapped[int]


class Date(Base):
    tablename = 'dates'

    id: Mapped[int] = mapped_column(primary_key = True)
    year: Mapped[int]
    month: Mapped[str] = mapped_column (String(10))


class Time(Base):
    tablename = 'times'

    id: Mapped[int] = mapped_column(primary_key = True)
    value: Mapped[str] = mapped_column(String(5))
 
 
class Book(Base):
    tablename = 'books'
 
    id: Mapped[int] = mapped_column(primary_key = True)
    date: Mapped[int] = mapped_column(ForeignKey('dates.id'))
    dey: Mapped[int]
    time: Mapped[str] = mapped_column(ForeignKey('times.id'))
    table: Mapped[int]
    quantity: Mapped[int]
    comment: Mapped[str] = mapped_column(String(125))
    user_ig: Mapped[int] = mapped_column(ForeignKey('users.tg_id'))


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
