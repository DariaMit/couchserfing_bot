from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btn_yes_rus = KeyboardButton('Да')
btn_no_rus = KeyboardButton('Нет')
change_invitation_rus = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
change_invitation_rus.add(btn_yes_rus, btn_no_rus)