from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from settings import BOT_TOKEN, HOST, USER, PASSWORD, DB_NAME, PORT
from db.postgresql_db import Database

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

db = Database(HOST, USER, PASSWORD, DB_NAME, PORT)
