from connect import bot,dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from handlers import UserAuthenticationState,EditState
from db import rename_user,edit_completed,edit_description,edit_delete


@dp.callback_query_handler(lambda query:query.data == 'имя')
async def get_rename(call:types.CallbackQuery,state:FSMContext):
    await bot.send_message(text='Введите новое имя',chat_id=call.from_user.id)
    await UserAuthenticationState.waiting_for_rename.set()

@dp.message_handler(state=UserAuthenticationState.waiting_for_rename)
async def set_rename(message:types.Message,state:FSMContext):
    await state.update_data(user_name = message.text,user_id = message.chat.id)
    data = await state.get_data()
    await rename_user(data)
    await bot.send_message(text= f"Вы успешно изменили имя {message.text}",chat_id=message.from_user.id)
    await state.finish()


@dp.callback_query_handler(state=EditState.waitin_for_bnt)
async def edit_data(call:types.CallbackQuery,state:FSMContext):
    message  = call.data
    if message == 'edit_bnt1':
        data = await state.get_data()
        await edit_completed(data)
        await bot.send_message(chat_id=call.from_user.id,text=f"Поздравляю с выполнением задачи")
        await state.finish()
    if message == 'edit_bnt2':
        await bot.send_message(chat_id=call.from_user.id,text="Введите новое осписание задачи")
        await EditState.waitin_for_edit_discription.set()
    if message == 'edit_bnt3':
        data = await state.get_data()
        await edit_delete(data)
        await state.finish()
@dp.message_handler(state=EditState.waitin_for_edit_discription)
async def input_new_description(message:types.Message,state:FSMContext):
    await state.update_data(new_desc=message.text)
    data = await state.get_data()
    await edit_description(data)
    await state.finish()


