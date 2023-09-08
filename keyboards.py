from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardMarkup,KeyboardButton,ReplyKeyboardRemove

ink_rename = InlineKeyboardMarkup()
bnt_rename = InlineKeyboardButton(text='Изменить имя',callback_data='имя')
ink_rename.add(bnt_rename)

ink_edit = InlineKeyboardMarkup()
bnt_completed = InlineKeyboardButton(text="состояние",callback_data="edit_bnt1")
bnt_decription = InlineKeyboardButton(text="описание",callback_data="edit_bnt2")
bnt_delete = InlineKeyboardButton(text="удалить",callback_data="edit_bnt3")
ink_edit.add(bnt_decription,bnt_completed,bnt_delete)

bnt_1 = KeyboardButton('/create📌')
bnt_2 = KeyboardButton('/show📝')
bnt_3 = KeyboardButton('/edit✏')
kb = ReplyKeyboardMarkup(resize_keyboard=True).row(bnt_1,bnt_2,bnt_3)

