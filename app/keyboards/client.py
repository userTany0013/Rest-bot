from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from datetime import date


async def menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='забронировать столик', callback_data='reserv')],
        [InlineKeyboardButton(text='мои брони', callback_data='my_ reserv')],
        [InlineKeyboardButton(text='контакты', callback_data='contacts')]
    ])


async def month():
    today = str(date.today())
    available_months = ...(today)
    keyboard = InlineKeyboardBuilder()
    for month in available_months:
        keyboard.add(InlineKeyboardButton(text=f'{month.name}',
                                           callback_data=f'month_{month.name}'))
    return keyboard.adjust(2).as_markup()


async def day():
    month = ...
    available_months = ...()
    keyboard = InlineKeyboardBuilder()
    for month in available_months:
        keyboard.add(InlineKeyboardButton(text=f'{month.name}',
                                           callback_data=f'month_{month.name}'))
    return keyboard.adjust(2).as_markup()
