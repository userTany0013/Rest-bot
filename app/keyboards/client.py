from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from datetime import date


menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='забронировать столик'),
     KeyboardButton(text='мои брони')],
    [KeyboardButton(text='контакты')]
],
resize_keyboard=True,
input_field_placeholder='Выберите пункт меню'
)


async def reg_name(first_name):
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=f'{first_name}')]
    ],
resize_keyboard=True,
input_field_placeholder='Отправте по кнопке или введите вручную'
)


async def reg_phone():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Поделиться контактом', request_contact=True)]
    ],
resize_keyboard=True,
input_field_placeholder='Введите номер'
)


async def month():
    today = str(date.today())
    available_months =await get_months(today)
    keyboard = InlineKeyboardBuilder()
    for month in available_months:
        keyboard.add(InlineKeyboardButton(text=f'{month.name}',
                                           callback_data=f'month_{month.id}'))
    return keyboard.adjust(2).as_markup()


async def day(month):
    today = str(date.today())
    available_days =await get_deys(today)
    keyboard = InlineKeyboardBuilder()
    for day in available_days:
        keyboard.add(InlineKeyboardButton(text=f'{day.name}',
                                           callback_data=f'month_{day.id}'))
    return keyboard.adjust(2).as_markup()


async def time(day):
    now = str(date.today())
    times =await get_times(now)
    keyboard = InlineKeyboardBuilder()
    for time in times:
        keyboard.add(InlineKeyboardButton(text=f'{time.name}',
                                           callback_data=f'month_{time.id}'))
    return keyboard.adjust(2).as_markup()


async def table(time):
    tables = await get_tables(time)
    keyboard = InlineKeyboardBuilder()
    for table in tables:
        keyboard.add(InlineKeyboardButton(text=f'{table.name}',
                                           callback_data=f'month_{table.id}'))
    return keyboard.adjust(2).as_markup()


async def comment():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Отправить без комментария', callback_data='no_comment')]
    ])


async def books(user):
    user_books = await get_books(user)
    keyboard = InlineKeyboardBuilder()
    for book in books:
        keyboard.add(InlineKeyboardButton(text=f'Дата:{book.month}, {book.day}\nВремя:{book.time}', callback_data=f'book_{book.id}'))
    return keyboard.adjust(2).as_markup()


async def change(book):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Изменить', callback_data=f'change_{book}')],
        [InlineKeyboardButton(text='Удалить', callback_data=f'delete_{book}')]
    ])


async def update(book):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Колличество', callback_data=f'quantity_{book}')],
        [InlineKeyboardButton(text='Комментарий', callback_data=f'comment_{book}')]
    ])


async def delete(book):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Да', callback_data=f'yes_{book}')],
        [InlineKeyboardButton(text='Нет', callback_data='no')]
    ])


async def admin(book):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Подтвердить', callback_data=f'confirm_{book}')],
        [InlineKeyboardButton(text='Удалить', callback_data=f'cancel_{book}')]
    ])
