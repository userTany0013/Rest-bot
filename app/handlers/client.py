from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards.client as kb


client = Router()


@client.message(CommandStart)
async def start_menu(message: Message, state: FSMContext):
    is_user = await set_user(message.from_user.id)
    if not is_user:
        await message.answer('Добро пожаловать! Пройдите регистрацию',
                             reply_markup=await kb.reg_name(message.from_user.first_name))
        await state.set_state('reg_name')
    else:
        await message.answer('Добро пожаловать! Выберите пункт меню:', reply_markup=await kb.menu())


@client.message(StateFilter('reg_name'))
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.capitalize())
    await state.set_state('reg_phone')
    await message.answer('Введите номер телефона:',
                         reply_markup=await kb.reg_phone())


@client.message(StateFilter('reg_phone'), F.contact)
async def register(message: Message, state: FSMContext):
    await state.update_data(name=message.contact.phone_number)
    data = await state.get_data()
    await update_user(message.from_user.id, data['name'], data['phone'])
    await message.answer('Вы зарегестрированы!', reply_markup=await kb.menu())


@client.message(F.text == 'забронировать столик')
async def reserv(message: Message, state: FSMContext):
    await message.answer('Выберите месяц:', reply_markup=await kb.month())
    await state.set_state('month')


@client.message(StateFilter('month'))
async def date(callback: CallbackQuery, state: FSMContext):
    await state.update_data(month=callback.data)
    await callback.message.answer('Выберите день:', reply_markup=await kb.day(callback.data))
    await state.set_state('day')


@client.message(StateFilter('day'))
async def day(callback: CallbackQuery, state: FSMContext):
    await state.update_data(day=callback.data)
    await callback.message.answer('Выберите время:', reply_markup=await kb.time(callback.data))
    await state.set_state('time')


@client.message(StateFilter('time'))
async def time(callback: CallbackQuery, state: FSMContext):
    await state.update_data(time=callback.data)
    await callback.message.answer('Выберите столик:', reply_markup=await kb.table(callback.data))
    await state.set_state('table')


@client.message(StateFilter('table'))
async def table(callback: CallbackQuery, state: FSMContext):
    await state.update_data(table=callback.data)
    await callback.message.answer('Введите колличество человек')
    await state.set_state('quantity')


@client.message(StateFilter('quantity'))
async def quantity(callback: CallbackQuery, state: FSMContext):
    await state.update_data(quantity=callback.data)
    await callback.message.answer('Добавте коментарий', reply_markup=await kb.comment())
    await state.set_state('comment')


@client.message(StateFilter('comment'))
async def comment(callback: CallbackQuery, state: FSMContext):
    user_name, user_phone = user(callback.from_user.id)
    data=await state.get_data()
    month=await data.get('month'),
    day=await data.get('day'),
    time=await data.get('time'),
    table=await data.get('table'),
    quantity=await data.get('quantity'),
    comment=callback.data
    await booking(month=month,
                  day=day,
                  time=time,
                  table=table,
                  quantity=quantity,
                  comment=comment)
    await state.clear()
    full_info = f'Клиент: {user_name}\n Номер телефона: {user_phone}\n Месяц: {month}\n Число: {day}\n Время: {time}\n Столик: {table}\n Колличество: {quantity}\n Комментарий: {comment}'
    await callback.message.bot.send_message(..., text=full_info)
    await callback.message.answer('Бронь добавлена, ожидайте подтверждения.', reply_markup=await kb.menu)


@client.message(F.text == 'мои брони')
async def my_books(message: Message):
    await message.answer('Ваши брони:', reply_markup=await kb.books(message.from_user.id))


@client.callback_query(F.data.startswith('book_'))
async def book(callback: CallbackQuery):
    book = await get_book(callback.data.split('_')[1])
    await callback.message.answer(
        f'Месяц: {book.month}\n Число: {book.day}\n Время: {book.time}\n Столик: {book.table}\n Колличество: {book.quantity}\n Комментарий: {book.comment}',
        reply_markup=await kb.change(callback.data.split('_')[1]))


@client.callback_query(F.data.startswith('change_'))
async def change(callback: CallbackQuery):
    await callback.message.answer('Выберите пункт меню:', reply_markup=await kb.update(callback.data.split('_')[1]))


@client.callback_query(F.data.startswith('quantity_'))
async def new_quantity(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите колличество человек:')
    state.update_data(book=callback.data.split('_')[1])
    state.set_state('new_quantity')


@client.message(StateFilter('new_quantity'))
async def add_quantity(message: Message, state: FSMContext):
    data = await state.get_data()
    book = await data.get('book')
    await update_quantity(book, message.text)
    await state.clear()
    await message.answer('Бронь изменена', reply_markup=await kb.books(message.from_user.id))


@client.callback_query(F.data.startswith('comment_'))
async def new_comment(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите новый комментарий:')
    state.update_data(book=callback.data.split('_')[1])
    state.set_state('new_comment')


@client.message(StateFilter('new_comment'))
async def add_comment(message: Message, state: FSMContext):
    data = await state.get_data()
    book = await data.get('book')
    await update_comment(book, message.text)
    await state.clear()
    await message.answer('Бронь изменена', reply_markup=await kb.books(message.from_user.id))


@client.callback_query(F.data.startswith('delete_'))
async def delete(callback: CallbackQuery):
    await callback.message.answer('Удалить эту бронь:', reply_markup=await kb.delete(callback.data.split('_')[1]))


@client.callback_query(F.data.startswith('yes_'))
async def delete(callback: CallbackQuery):
    await delete_book(callback.data.split('_')[1])
    await callback.message.answer('Бронь удалена', reply_markup=await kb.books(callback.message.from_user.id))

@client.callback_query(F.data.startswith('no_'))
async def no_delete(callback: CallbackQuery):
    await callback.message.answer('Ваши брони:', reply_markup=await kb.books(callback.from_user.id))
