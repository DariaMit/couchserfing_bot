import config
import logging
from aiogram import Bot, Dispatcher
from db_mysql import Database
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

token = config.TG_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)

db = Database('bot_db')