from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards.client as kb


client = Router()


@client.message(CommandStart)
async def start_menu(message: Message):
    await message.answer('Добро пожаловать! Выберите пункт меню:', reply_markup=await kb.menu())


@client.callback_query(F.data == 'reserv')
async def resrrv(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Выберите месяц:', reply_markup=await kb.month())
    await state.set_state('month')


@client.callback_query(StateFilter('month'))
async def date(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Выберите день:', reply_markup=await kb.day())