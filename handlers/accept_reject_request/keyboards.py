from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

accept_reject_callback = CallbackData('accept_reject', 'answer', 'guest_id')

def get_keyboard_for_host(guest_id):
    accept_reject_keyboard = InlineKeyboardMarkup()
    btn_share_contacts = InlineKeyboardButton(text='Поделиться контактами',
                                              callback_data=accept_reject_callback.new(answer='share', guest_id=guest_id))
    accept_reject_keyboard.insert(btn_share_contacts)
    return accept_reject_keyboard
