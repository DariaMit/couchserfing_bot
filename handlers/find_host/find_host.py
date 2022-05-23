from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from couch_bot1.create_bot import bot, db
from couch_bot1.handlers.start import FSMUsage
from couch_bot1.handlers.find_host.keyboards import get_keyboard_for_host, get_keyboard_send_request


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
    await FSMUsage.next()
    if all_hosts == 'В этом городе нет доступных хостов':
        await state.finish()
    else:
        host_id = all_hosts[data.get('hosts_count')][0]
        await bot.send_message(message.from_user.id, format_reply(all_hosts[data.get('hosts_count')]),
                               reply_markup=get_keyboard_send_request(host_id), parse_mode='HTML') #вставить туда ссылку на хостов



async def send_request(call: types.CallbackQuery):
    callback_data = call.data
    print(callback_data)
    host_id = str(callback_data).split(':')[-1]
    await call.message.answer('Напишите текст запроса')
    await bot.send_message(host_id, 'Это сообщение должно было прийти Кате, напишите, кому пришло')



def register_handlers_find_host(dp: Dispatcher):
    dp.register_message_handler(find_host, commands=['findhost'])
    dp.register_message_handler(searched_city, state=FSMUsage.searched_city)
    dp.register_callback_query_handler(send_request, lambda callback_query: True)