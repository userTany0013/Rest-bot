from app.database.models import async_session, Book, Image

from sqlalchemy import select, update


async def update_status(book, status):
 async with async_session as session:
  await session.execute(update(Book).where(Book.id==book).values(status=status))
  await session.commit()


async def get_user_id(book):
 async with async_session() as session:
  book = session.scalar(select(Book).where(Book.id==book))
  return await book.user_tg
  
  
async def get_book(book):
 async with async_session() as session:
  return await session.scalar(select(Book).where(Book.id==book))
 

async def image_set(image_id):
  async with async_session() as session:
   session.add(Image(tg_id=image_id))
   await session.commit()
