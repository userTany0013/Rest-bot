from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards.admin as kb


admin = Router()


@admin.callback_query(F.data.startswith('confirm_'))
async def confirm(callback: CallbackQuery):
    await update_status(callback.data.split('_')[1], 'confirm')
    user_id = get_user_id(callback.data.split('_')[1])
    book = get_book(callback.data.split('_')[1])
    await callback.message.bot.send_message(user_id, text=f'Бронь подтверждена:\n\n Месяц: {book.month}\n Число: {book.day}\n Время: {book.time}\n Столик: {book.table}\n Колличество: {book.quantity}\n Комментарий: {book.comment}')
    await callback.message.answer('Бронь подтверждена')


@admin.callback_query(F.data.startswith('cancel_'))
async def cancel(callback: CallbackQuery):
    await callback.message.answer('Выберите причину:', reply_markup=await kb.cancel(callback.data.split('_')[1]))


@admin.callback_query(F.data.startswith('occupied_'))
async def occupied(callback: CallbackQuery):
    await update_status(callback.data.split('_')[1], 'cancel')
    user_id = get_user_id(callback.data.split('_')[1])
    book = get_book(callback.data.split('_')[1])
    await callback.message.bot.send_message(user_id, text=f'Сожалеем, бронь уже занята:\n\n Месяц: {book.month}\n Число: {book.day}\n Время: {book.time}\n Столик: {book.table}\n Колличество: {book.quantity}\n Комментарий: {book.comment}')
    await callback.message.answer('Бронь отменена')


@admin.callback_query(F.data.startswith('reason_'))
async def enter_reason(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Ведите причину:')
    await state.update_data(book_id=callback.data.split('_')[1])
    await state.set_state('reason')


@admin.message(StateFilter('reason'))
async def reason(message: Message, state: FSMContext):
    data = await state.get_data()
    book_id = await data.get(book_id)
    await update_status(book_id, 'cancel')
    user_id = get_user_id(book_id)
    book = get_book(book_id)
    cancel_reason = message.text
    await message.bot.send_message(user_id, text=f'Сожалеем, запись отменена по причине:\n{cancel_reason}\n\n Месяц: {book.month}\n Число: {book.day}\n Время: {book.time}\n Столик: {book.table}\n Колличество: {book.quantity}\n Комментарий: {book.comment}')
    await message.answer('Бронь отменена')
    await state.clear()
