from aiogram import Bot,Dispatcher,executor
from aiogram import Bot,Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
TOKEN_API = "6225525226:AAGtxRMS8OYIXZNA8zBRDowjhzoUd45h8xk"
bot = Bot(TOKEN_API)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)