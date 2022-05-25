from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from couch_bot1.create_bot import bot, db
from .keyboards import language_choice, main_menu_rus, change_invitation_rus


class FSMStart(StatesGroup):
    pass

class FSMUsage(StatesGroup):
    language = State()
    vk_link = State()
    is_host = State()
    menu = State()
    searched_city = State()
    choosing_host = State()
    write_text = State()
    send_request = State()
    already_host = State()
    host_city = State()
    write_inv_text = State()
    end_inv = State()
    leave_review = State()
    write_review_text = State()
    leave_mark = State()


async def start(message: types.Message, state: FSMContext):
    if not db.user_exists(message.from_user.id):
        await FSMUsage.language.set()
        await bot.send_message(message.from_user.id, 'Choose your language. Выберите язык', reply_markup=language_choice)
    else:
        await FSMUsage.menu.set()
        async with state.proxy() as data:
            data['lang'] = 0 if db.get_lang(message.from_user.id) == 'Русский' else 1
        await bot.send_message(message.from_user.id, 'Привет! Выбери, что хочешь сделать', reply_markup=main_menu_rus)

async def show_main_menu(message: types.Message, state: FSMContext):
    if message.text == 'Найти хоста':
        await FSMUsage.searched_city.set()
        await bot.send_message(message.from_user.id, 'В каком городе ты ищешь хоста?')
    elif message.text == 'Создать объявление':
        if db.user_invitation_exists(message.from_user.id):
            async with state.proxy() as data:
                data['changing'] = True
            await FSMUsage.already_host.set()
            await bot.send_message(message.from_user.id, 'Вы уже создали приглашение. Хотите его изменить?', reply_markup=change_invitation_rus)
        else:
            async with state.proxy() as data:
                data['changing'] = False
            await FSMUsage.host_city.set()
            await bot.send_message(message.from_user.id, 'В каком городе ты принимаешь гостей?')
    elif message.text == 'Оставить отзыв на хоста':
        await FSMUsage.leave_review.set()
        await bot.send_message(message.from_user.id, 'Отправьте юзернейм хоста в ТГ или ссылку в ВК, на которого вы хотели бы оставить отзыв\n(напр. "@privet или vk.com/privet)')



def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], state='*')
    dp.register_message_handler(show_main_menu, state=FSMUsage.menu)