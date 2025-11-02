from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def cancel(book):
        return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Занята', callback_data=f'occupied_{book}')],
        [InlineKeyboardButton(text='Другая причина', callback_data=f'reason_{book}')]
    ])
