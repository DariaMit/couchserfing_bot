from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

accept_reject_callback = CallbackData('accept_reject', 'answer', 'guest_id')
send_request_callback = CallbackData('send_or_more', 'action', 'host_id')

def get_keyboard_for_host(guest_id):
    accept_reject_keyboard = InlineKeyboardMarkup()
    btn_share_contacts = InlineKeyboardButton(text='Поделиться контактами',
                                              callback_data=accept_reject_callback.new(answer='share', guest_id=guest_id))
    accept_reject_keyboard.insert(btn_share_contacts)
    return accept_reject_keyboard

def get_keyboard_send_request(host_id):
    send_or_more_keyboard = InlineKeyboardMarkup()
    btn_more = InlineKeyboardButton(text='Ещё', callback_data=send_request_callback.new(action='next_host', host_id=False))
    btn_send_request = InlineKeyboardButton(text='Отправить запрос', callback_data=send_request_callback.new(action='send_request', host_id=host_id))
    send_or_more_keyboard.insert(btn_more)
    send_or_more_keyboard.insert(btn_send_request)
    return send_or_more_keyboard