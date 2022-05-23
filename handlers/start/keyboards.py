from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



#Выбор языка
btn_eng = KeyboardButton('Русский')
btn_rus = KeyboardButton('Русский')
language_choice = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
language_choice.add(btn_rus, btn_eng)

#Главное меню
#Русский язык
btn_settings_rus = KeyboardButton('Настройки')
btn_find_host_rus = KeyboardButton('Найти хоста')
btn_create_invitation_rus = KeyboardButton('Создать объявление')
btn_leave_review_rus = KeyboardButton('Оставить отзыв на хоста')
main_menu_rus = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
main_menu_rus.add(btn_settings_rus, btn_find_host_rus, btn_create_invitation_rus, btn_leave_review_rus)

btn_yes_rus = KeyboardButton('Да')
btn_no_rus = KeyboardButton('Нет')
change_invitation_rus = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
change_invitation_rus.add(btn_yes_rus, btn_no_rus)