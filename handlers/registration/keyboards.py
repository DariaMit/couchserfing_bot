from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

#Принимает ли гостей. Создано две клавиатуры в зависимости от языка. Внутри функции выбираем нужную
#Русский язык
btn_yes_rus = KeyboardButton('Да')
btn_no_rus = KeyboardButton('Нет')
is_host_menu_rus = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
is_host_menu_rus.add(btn_yes_rus, btn_no_rus)