from connect import bot,dp
from aiogram import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import handlers
import callbacks

if __name__ == '__main__':
     executor.start_polling(dp,skip_updates=True)