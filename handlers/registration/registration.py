from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from well_another.create_bot import bot, db
import requests
import couch_bot1.config as config
from couch_bot1.handlers.start import FSMUsage
from .keyboards import is_host_menu_rus


async def language(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['language'] = message.text
        data['lang'] = 0 if message.text == 'Русский' else 1
    await FSMUsage.next()
    resp = ['Оставь ссылку на страницу вк']
    await bot.send_message(message.from_user.id, resp)


async def link(message: types.Message, state: FSMContext):
    if 'vk.com/' not in message.text:
        await bot.send_message(message.from_user.id, 'Ссылка недействительна! Отправьте действительную :)))')
    else:
        id = message.text.split('/')[-1]
        res = requests.get(f'https://api.vk.com/method/users.get?user_ids={id}&fields=sex,bdate&v=5.131&access_token={config.vk_user_token}')
        json = res.json()
        async with state.proxy() as data:
            data['name'] = f'{json["response"][0]["first_name"]} {json["response"][0]["last_name"]}'
            data['vk_id'] = id
            if 'bdate' in json["response"][0]:
                data['bdate'] = f'{json["response"][0]["bdate"]}'
        await FSMUsage.next()
        await bot.send_message(message.from_user.id, 'Вы готовы принимать гостей?', reply_markup=is_host_menu_rus)


async def is_host(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['is_host'] = message.text
        language = data.get('language')
        name = data.get('name')
        vk_id = data.get('vk_id')
        bdate = data.get('bdate')
        is_host = 1 if data.get('is_host') == 'Да' else 0
        username_TG = message.from_user.username
        db.add_all_for_registration(message.from_user.id, vk_id, name, is_host, language, bdate, username_TG)
    await bot.send_message(message.from_user.id, 'Регистрация завершена!')
    await state.finish()


def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(language, state=FSMUsage.language)
    dp.register_message_handler(link, state=FSMUsage.vk_link)
    dp.register_message_handler(is_host, state=FSMUsage.is_host)