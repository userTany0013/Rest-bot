from aiogram import Router, F
from aiogram.filters import StateFilter, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards.admin as kb
from app.database.requests.admin import update_status, get_user_id, get_book, image_set, delete_book


admin = Router()


@admin.callback_query(F.data.startswith('confirm_'))
async def confirm(callback: CallbackQuery):
    await update_status(callback.data.split('_')[1], 'confirm')
    user_id = await get_user_id(callback.data.split('_')[1])
    book = await get_book(callback.data.split('_')[1])
    await callback.message.bot.send_message(user_id, text=f'Бронь подтверждена:\n\n Месяц: {book.date}\n Число: {book.day}\n Время: {book.time}\n Столик: {book.table}\n Колличество: {book.quantity}\n Комментарий: {book.comment}')
    await callback.message.answer('Бронь подтверждена')


@admin.callback_query(F.data.startswith('cancel_'))
async def cancel(callback: CallbackQuery):
    await callback.message.answer('Выберите причину:', reply_markup=await kb.cancel(callback.data.split('_')[1]))


@admin.callback_query(F.data.startswith('occupied_'))
async def occupied(callback: CallbackQuery):
    user_id = await get_user_id(callback.data.split('_')[1])
    book = await get_book(callback.data.split('_')[1])
    await callback.message.bot.send_message(user_id, text=f'Сожалеем, бронь уже занята:\n\n Месяц: {book.date}\n Число: {book.day}\n Время: {book.time}\n Столик: {book.table}\n Колличество: {book.quantity}\n Комментарий: {book.comment}')
    await delete_book(callback.data.split('_')[1])
    await callback.message.answer('Бронь отменена')


@admin.callback_query(F.data.startswith('reason_'))
async def enter_reason(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Ведите причину:')
    await state.update_data(book_id=callback.data.split('_')[1])
    await state.set_state('reason')


@admin.message(StateFilter('reason'))
async def reason(message: Message, state: FSMContext):
    data = await state.get_data()
    book_id = data.get('book_id')
    user_id = await get_user_id(book_id)
    book = await get_book(book_id)
    cancel_reason = message.text
    await message.bot.send_message(user_id, text=f'Сожалеем, запись отменена по причине:\n{cancel_reason}\n\n Месяц: {book.date}\n Число: {book.day}\n Время: {book.time}\n Столик: {book.table}\n Колличество: {book.quantity}\n Комментарий: {book.comment}')
    await delete_book(book_id)
    await message.answer('Бронь отменена')
    await state.clear()


@admin.message(Command('now_image'))
async def now_image(massage: Message, state: FSMContext):
 await massage.answer('Отправте новое фото:')
 await state.set_state('image')


@admin.message(F.photo, StateFilter('image'))
async def set_image(massage: Message, state: FSMContext):
 image_id = massage.photo[-1].file_id
 await image_set(image_id)
 await massage.answer('Фото добавлено')
 state.clear()
