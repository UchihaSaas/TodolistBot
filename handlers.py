from db import add_user,check_user,set_task,show_todolist
from connect import bot, dp
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboards import ink_rename,kb,ink_edit
from aiogram.types import ParseMode
class UserAuthenticationState(StatesGroup):
    waiting_for_name = State()
    waiting_for_rename = State()
class TaskState(StatesGroup):
    waitin_for_discription = State()
class EditState(StatesGroup):
    waitin_for_id = State()
    waitin_for_bnt = State()
    waitin_for_edit_discription = State()

@dp.message_handler(commands=['start'])
async def start_bot(message:types.Message):
    await message.answer('What''s up,The Bot has been started',reply_markup=kb)

@dp.message_handler(commands=['edit✏'])
async def edit_task(message:types.Message,state:FSMContext):
    await message.answer("Введите id задачи которую хотите изменить")
    await EditState.waitin_for_id.set()

@dp.message_handler(state=EditState.waitin_for_id)
async def input_id(message:types.Message,state:FSMContext):
    edit_task_id  = message.text
    await state.update_data(user_id = message.chat.id,edit_task_id = edit_task_id)
    await bot.send_message(chat_id=message.from_user.id,text="Отлично что вы хотите изменить",reply_markup=ink_edit)
    await EditState.waitin_for_bnt.set()


@dp.message_handler(commands=['create📌'])
async def create_task(message:types.Message,state:FSMContext):
    await message.answer("Опишите вашу задачу")
    await TaskState.waitin_for_discription.set()

@dp.message_handler(state= TaskState.waitin_for_discription)
async def set_create_task(message:types.Message,state:FSMContext):
    await state.update_data(task_desctiption = message.text,user_id = message.chat.id)
    data = await state.get_data()
    await set_task(data)
    await bot.send_message(chat_id=message.from_user.id,text="УСПЕХ")
    await state.finish()


@dp.message_handler(commands=['show📝'])
async def show_list(message: types.Message):
    user_id = message.chat.id
    result = await show_todolist(user_id)
    output = ""
    for row in result:
        output += f"{row[0]} ID: <i>{row[1]}</i>: <b>{row[2]}</b>\n".replace("False", "❌").replace("True","✅")
    await bot.send_message(message.from_user.id, text=output, parse_mode=ParseMode.HTML)

@dp.message_handler(commands=['profile'])
async def get_profile(message: types.Message):
    response = await check_user(message.chat.id)
    await bot.send_message(chat_id=message.from_user.id, text=response)


@dp.message_handler(commands=['registration'])
async def registration_command(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, text='Введите свое имя')
    await UserAuthenticationState.waiting_for_name.set()

@dp.message_handler(state=UserAuthenticationState.waiting_for_name)
async def set_name(message: types.Message, state: FSMContext):
    user_name = str(message.text)
    if len(user_name) > 128:
        await bot.send_message(chat_id=message.from_user.id, text='Неверный формат имени')
    else:
        await state.update_data(user_name=message.text, user_id=message.chat.id)
        data = await state.get_data()
        result = await add_user(data, data['user_id'])
        if result == "User already exists.":
            await bot.send_message(chat_id=message.from_user.id, text='Вы уже зарегистрированы',reply_markup=ink_rename)
        elif result == "User added successfully.":
            await bot.send_message(chat_id=message.from_user.id, text='Вы успешно зарегистрированы')
        else:
            await bot.send_message(chat_id=message.from_user.id, text='Произошла ошибка при регистрации')
        await state.finish()

