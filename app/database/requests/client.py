from app.database.models import async_session, Date, Time, Book, User, Table

from sqlalchemy import select, update, delete

from datetime import datetime
from calendar import monthrange


async def get_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return True if user else False
    

async def set_user(tg_id, name, phone):
    async with async_session() as session:
        session.add(User(tg_id=tg_id, name=name, phone=phone))
        await session.commit()


async def user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id==tg_id))
        return user.name, user.phone
    

async def booking(user_id, month, day, time, table, quantity, comment):
    async with async_session() as session:
        date = await session.scalar(select(User).where(Date.id==month))
        session.add(Book(user_id=user_id,
                  date=date.id,
                  day=day,
                  time=time,
                  table=table,
                  quantity=quantity,
                  comment=comment))
        await session.commit()


async def get_book(book):
    async with async_session() as session:
        return await session.scalar(select(Book).where(Book.id==book))


async def update_quantity(book, message_text):
    async with async_session() as session:
        await session.execute(update(Book).where(Book.id==book).values(quantity=message_text))
        await session.commit()


async def update_comment(book, message_text):
    async with async_session() as session:
        await session.execute(update(Book).where(Book.id==book).values(comment=message_text))
        await session.commit()


async def delete_book(book):
    async with async_session() as session:
        await session.delete(select(Book).where(Book.id==book))
        await session.commit()


async def get_months():
    async with async_session() as session:
        dates = []
        year = datetime.now().year
        month = datetime.now().month
        now = await session.scalar(select(Date).where(Date.year==year, Date.month==month))
        months = await session.scalars(select(Date))
        for mon in months:
            if mon.id >= now.id:
                dates.append(mon)
        return dates


async def get_deys(month_):
    async with async_session() as session:
        days = []
        date = await session.scalar(select(Date).where(Date.id==month_))
        days_in_month = monthrange(date.year, date.month)[1]
        month_now = datetime.now().month
        if month_now == date.month:
            date = datetime.now().day
            for day in range[date:days_in_month]:
                days.append(day)
        else:
            for day in range[:days_in_month]:
                days.append(day)
        return days


async def get_times(day, monts):
    async with async_session() as session:
        times = []
        times_in_dey = await session.scalars(select(Time))
        monts_now = datetime.now().month
        day_now = datetime.now().day
        if monts_now == monts:
            if day_now == day:
                now = datetime.now().time()
                for time in times_in_dey:
                    if time > now:
                        times.append(time)
            else:
                for time in times_in_dey:
                    times.append(time)
        else:
            for time in times_in_dey:
                times.append(time)
        return times


async def get_tables(time, day, monts):
    async with async_session() as session:
        all_tables = []
        tables = await session.scalars(select(Table))
        occupied = await session.scalars(select(Book).where(Book.date==monts, Book.day==day, Book.time==time))
        occupied_tables = []
        for book in occupied:
            occupied_tables.append(book.table)
        for table in tables:
            if table.id not in occupied_tables:
                all_tables.append(table.id)
        return all_tables


async def get_books(user):
    async with async_session() as session:
        return await session.scalars(select(Book).where(Book.user_tg==user))
