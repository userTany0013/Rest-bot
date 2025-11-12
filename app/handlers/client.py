from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards.client as kb

from data import ADMIN_GROUP

from app.database.requests.client import get_user, set_user, user_get, booking, get_book, update_quantity, update_comment, delete_book, photo_id


client = Router()


@client.callback_query(F.data  == 'back_menu')
@client.message(CommandStart())
async def start_menu(event: Message | CallbackQuery, state: FSMContext):
    if isinstance(event, Message):
        is_user = await get_user(event.from_user.id)
        if not is_user:
            await event.answer('Добро пожаловать! Пройдите регистрацию',
                                reply_markup=await kb.reg_name(event.from_user.first_name))
            await state.set_state('reg_name')
        else:
            await event.answer('Добро пожаловать! Выберите пункт меню:', reply_markup=kb.menu)
    else:
        await state.clear()
        await event.message.answer('Выберите пункт меню:', reply_markup=kb.menu)


@client.message(StateFilter('reg_name'))
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.capitalize())
    await state.set_state('reg_phone')
    await message.answer('Введите номер телефона:',
                         reply_markup=await kb.reg_phone())


@client.message(StateFilter('reg_phone'), F.contact)
async def register(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    data = await state.get_data()
    await set_user(message.from_user.id, data['name'], data['phone'])
    await message.answer('Вы зарегестрированы!', reply_markup=kb.menu)


@client.callback_query(F.data  == 'back_month')
@client.message(F.text == 'забронировать столик')
async def reserv(event: Message | CallbackQuery, state: FSMContext):
    if isinstance(event, Message):
        await event.answer('Выберите месяц:', reply_markup=await kb.month())
        await state.set_state('month')
    else:
        await state.clear()
        await event.message.answer('Выберите месяц:', reply_markup=await kb.month())
        await state.set_state('month')


@client.callback_query(F.data  == 'back_day')
@client.callback_query(StateFilter('month'), F.data.startswith('month_'))
async def date(callback: CallbackQuery, state: FSMContext):
    if callback.data.startswith('month_'):
        await state.update_data(month=callback.data.split('_')[1])
        await callback.message.answer('Выберите день:', reply_markup=await kb.day(callback.data.split('_')[1]))
    else:
        data = await state.get_data()
        month = data.get('month')
        await callback.message.answer('Выберите день:', reply_markup=await kb.day(month))
    await state.set_state('day')



@client.callback_query(F.data  == 'back_time')
@client.callback_query(StateFilter('day'), F.data.startswith('day_'))
async def day(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    month = data.get('month')
    if callback.data.startswith('day_'):
        await state.update_data(day=callback.data.split('_')[1])
        await callback.message.answer('Выберите время:', reply_markup=await kb.time(callback.data.split('_')[1], month))
    else:
        day = data.get('day')
        await callback.message.answer('Выберите время:', reply_markup=await kb.time(day, month))
    await state.set_state('time')


@client.callback_query(F.data  == 'back_table')
@client.callback_query(StateFilter('time'), F.data.startswith('time_'))
async def time(callback: CallbackQuery, state: FSMContext):
    image = await photo_id()
    data = await state.get_data()
    month = data.get('month')
    day = data.get('day')
    if callback.data.startswith('time_'):
        await state.update_data(time=callback.data.split('_')[1])
        await callback.message.answer_photo(photo=image.tg_id, caption='Выберите столик:', reply_markup=await kb.table(callback.data.split('_')[1], day, month))
    else:
        time = data.get('time')
        await callback.message.answer_photo(photo=image.tg_id, caption='Выберите столик:', reply_markup=await kb.table(time, day, month))
    await state.set_state('table')


@client.callback_query(StateFilter('table'), F.data.startswith('table_'))
async def table(callback: CallbackQuery, state: FSMContext):
    await state.update_data(table=callback.data.split('_')[1])
    await callback.message.answer('Введите колличество человек')
    await state.set_state('quantity')


@client.message(StateFilter('quantity'))
async def quantity(message: Message, state: FSMContext):
    await state.update_data(quantity=message.text)
    await message.answer('Добавте коментарий', reply_markup=await kb.comment())
    await state.set_state('comment')


@client.callback_query(StateFilter('comment'), F.data == 'no_comment')
@client.message(StateFilter('comment'))
async def comment(event: Message | CallbackQuery, state: FSMContext):
    if isinstance(event, Message):
        comment=event.text
    else:
        comment=event.data
    user =await user_get(event.from_user.id)
    data=await state.get_data()
    month=data['month']
    day=data['day']
    time=data['time']
    table=data['table']
    quantity=data['quantity']
    book_obj = await booking(month, day, time, table, quantity, comment, user.tg_id)
    await state.clear()
    print(book_obj)
    full_info = f'Клиент: {user.name}\n Номер телефона: {user.phone}\n Месяц: {month}\n Число: {day}\n Время: {time}\n Столик: {table}\n Колличество: {quantity}\n Комментарий: {comment}'
    if isinstance(event, Message):
        await event.bot.send_message(ADMIN_GROUP, text=full_info, reply_markup=await kb.admin(book_obj))
        await event.answer('Бронь добавлена, ожидайте подтверждения.', reply_markup=kb.menu)
    else:
        await event.message.bot.send_message(ADMIN_GROUP, text=full_info, reply_markup=await kb.admin(book_obj))
        await event.message.answer('Бронь добавлена, ожидайте подтверждения.', reply_markup=kb.menu)


@client.message(F.text == 'мои брони')
async def my_books(message: Message):
    await message.answer('Ваши брони:', reply_markup=await kb.books(message.from_user.id))


@client.callback_query(F.data.startswith('book_'))
async def book(callback: CallbackQuery):
    book = await get_book(callback.data.split('_')[1])
    await callback.message.answer(
        f'Месяц: {book.date}\n Число: {book.day}\n Время: {book.time}\n Столик: {book.table}\n Колличество: {book.quantity}\n Комментарий: {book.comment}',
        reply_markup=await kb.change(callback.data.split('_')[1]))


@client.callback_query(F.data.startswith('change_'))
async def change(callback: CallbackQuery):
    await callback.message.answer('Выберите пункт меню:', reply_markup=await kb.update(callback.data.split('_')[1]))


@client.callback_query(F.data.startswith('quantity_'))
async def new_quantity(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите колличество человек:')
    await state.update_data(book=callback.data.split('_')[1])
    await state.set_state('new_quantity')


@client.message(StateFilter('new_quantity'))
async def add_quantity(message: Message, state: FSMContext):
    data = await state.get_data()
    book = data.get('book')
    await update_quantity(book, message.text)
    await state.clear()
    await message.answer('Бронь изменена', reply_markup=await kb.books(message.from_user.id))


@client.callback_query(F.data.startswith('comment_'))
async def new_comment(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите новый комментарий:')
    await state.update_data(book=callback.data.split('_')[1])
    await state.set_state('new_comment')


@client.message(StateFilter('new_comment'))
async def add_comment(message: Message, state: FSMContext):
    data = await state.get_data()
    book = data.get('book')
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

@client.callback_query(F.data.startswith('no'))
async def no_delete(callback: CallbackQuery):
    await callback.message.answer('Ваши брони:', reply_markup=await kb.books(callback.from_user.id))
