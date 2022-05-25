from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from couch_bot1.create_bot import bot, db

from couch_bot1.handlers.start import FSMUsage
from couch_bot1.handlers.find_host.keyboards import get_keyboard_for_host, get_keyboard_send_request, send_request_callback



async def find_host(message: types.Message):
    await FSMUsage.searched_city.set()
    await bot.send_message(message.from_user.id, 'В каком городе ты ищешь хоста?')


async def searched_city(message: types.Message, state: FSMContext):
    all_hosts = db.get_host_by_city(message.text)

    def format_reply(reply):
        return f'<b>{reply[1]}</b>\n{reply[2]}'

    async with state.proxy() as data:
        data['city'] = message.text
        data['all_hosts'] = all_hosts
        data['hosts_count'] = 0
    if all_hosts == 'В этом городе нет доступных хостов':
        await bot.send_message(message.from_user.id, 'В этом городе нет доступных хостов')
    else:
        await FSMUsage.next()
        host_id = all_hosts[data.get('hosts_count')][0]
        await bot.send_message(message.from_user.id, format_reply(all_hosts[data.get('hosts_count')]),
                               reply_markup=get_keyboard_send_request(host_id), parse_mode='HTML')


async def watch_host_reviews(call: types.CallbackQuery, state: FSMContext):
    callback_data = call.data
    host_id_db = str(callback_data).split(':')[-1]
    last_reviews = db.get_host_reviews(host_id_db)
    def format_reviews(all_reviews):
        answer = ''
        i = 1
        for review in all_reviews:
            answer += f'{i}) {review[0]}\n\n'
            i += 1
        print(answer)
        return answer

    await call.message.answer(format_reviews(last_reviews))



async def write_text(call: types.CallbackQuery, state: FSMContext):
    callback_data = call.data
    host_id_db = str(callback_data).split(':')[-1]
    host_id_tg = db.get_TG_id(host_id_db)
    async with state.proxy() as data:
        data['host_to_send'] = host_id_tg
    await call.message.answer('Напишите текст запроса')
    await FSMUsage.next()


async def next_host(call: types.CallbackQuery, state: FSMContext):
    def format_reply(reply):
        return f'<b>{reply[1]}</b>\n{reply[2]}'

    async with state.proxy() as data:
        data['hosts_count'] += 1
    if data.get('hosts_count') == len(data.get('all_hosts')):
        reply = 'Больше нет доступных хостов в этом городе'
        keyboard = None
        await state.finish()
    else:
        host_id = data.get('all_hosts')[data.get('hosts_count')][0]
        host_info = data.get('all_hosts')[data.get('hosts_count')]
        reply = format_reply(host_info)
        keyboard = get_keyboard_send_request(host_id)
    await call.message.answer(reply, reply_markup=keyboard,
                              parse_mode='HTML')


async def send_request(message: types.Message, state: FSMContext):
    text_to_send = message.text
    async with state.proxy() as data:
        host_id = data.get('host_to_send')
    print(host_id)
    await bot.send_message(host_id, f'Пользователь @{message.from_user.username} отправляет Вам запрос на заселиться потусить:\n{text_to_send}', reply_markup=get_keyboard_for_host(message.from_user.id))
    await bot.send_message(message.from_user.id, 'Ваш запрос отправлен. Как только хост решит поделиться контактами, мы Вам сообщим')
    await FSMUsage.choosing_host.set()



def register_handlers_find_host(dp: Dispatcher):
    dp.register_message_handler(find_host, commands=['findhost'], state='*')
    dp.register_message_handler(searched_city, state=FSMUsage.searched_city)
    dp.register_callback_query_handler(write_text, send_request_callback.filter(action='send_request'), state='*')
    dp.register_callback_query_handler(next_host, send_request_callback.filter(action='next_host'), state='*')
    dp.register_callback_query_handler(watch_host_reviews, send_request_callback.filter(action='watch_reviews'), state='*')
    dp.register_message_handler(send_request, state=FSMUsage.write_text)

