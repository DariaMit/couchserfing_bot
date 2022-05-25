from aiogram import types, Dispatcher
from couch_bot1.create_bot import bot, db
import logging
from .keyboards import accept_reject_callback


async def share_contacts_with_guest(call: types.CallbackQuery):
    callback_data = call.data
    guest_id = str(callback_data).split(':')[-1]
    logging.info(f'call = {callback_data}')
    await call.message.answer('Ваши контакты переданы!')
    host_info = db.get_host_info(call.from_user.id)
    host_vk = host_info[0]
    host_name = host_info[1]
    host_tg = call.from_user.username
    await bot.send_message(guest_id, f'{host_name} делится с Вами контактами:\nВК: vk.com/{host_vk}\nTelegram: @{host_tg}')




def register_handlers_share_contacts(dp: Dispatcher):
    dp.register_callback_query_handler(share_contacts_with_guest, accept_reject_callback.filter(answer='share'), state='*')