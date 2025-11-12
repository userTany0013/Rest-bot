from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests.client import get_months, get_deys, get_times, get_tables, get_books, get_time


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
    available_months =await get_months()
    keyboard = InlineKeyboardBuilder()
    for month in available_months:
        keyboard.add(InlineKeyboardButton(text=f'{month.month}',
                                           callback_data=f'month_{month.id}'))
    keyboard.add(InlineKeyboardButton(text=f'Назад', callback_data='back_menu'))
    return keyboard.adjust(2).as_markup()


async def day(month):
    available_days =await get_deys(month)
    keyboard = InlineKeyboardBuilder()
    for day in available_days:
        keyboard.add(InlineKeyboardButton(text=f'{day}',
                                           callback_data=f'day_{day}'))
    keyboard.add(InlineKeyboardButton(text=f'Назад', callback_data='back_month'))
    return keyboard.adjust(2).as_markup()


async def time(day, month):
    times =await get_times(day, month)
    print('!')
    print(times)
    keyboard = InlineKeyboardBuilder()
    for time in times:
        ti = await get_time(time)
        keyboard.add(InlineKeyboardButton(text=f'{ti.hour}, {ti.minute}',
                                           callback_data=f'time_{time}'))
    keyboard.add(InlineKeyboardButton(text=f'Назад', callback_data='back_day'))
    return keyboard.adjust(2).as_markup()


async def table(time, day, month):
    tables = await get_tables(time, day, month)
    keyboard = InlineKeyboardBuilder()
    for table in tables:
        keyboard.add(InlineKeyboardButton(text=f'{table}',
                                           callback_data=f'table_{table}'))
    keyboard.add(InlineKeyboardButton(text=f'Назад', callback_data='back_time'))
    return keyboard.adjust(2).as_markup()


async def comment():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Отправить без комментария', callback_data='no_comment')],
        [InlineKeyboardButton(text=f'Назад', callback_data='back_table')]
    ])


async def books(user):
    user_books = await get_books(user)
    keyboard = InlineKeyboardBuilder()
    for book in user_books:
        keyboard.add(InlineKeyboardButton(text=f'Дата:{book.date}, {book.day}\nВремя:{book.time}', callback_data=f'book_{book.id}'))
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
