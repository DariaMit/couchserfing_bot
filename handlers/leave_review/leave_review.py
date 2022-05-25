from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from couch_bot1.create_bot import bot, db
from couch_bot1.handlers.start import FSMUsage
from datetime import datetime


async def leave_review(message: types.Message):
    await FSMUsage.leave_review.set()
    await bot.send_message(message.from_user.id, 'Отправьте юзернейм хоста в ТГ или ссылку в ВК, на которого вы хотели бы оставить отзыв\n(напр. "@privet или vk.com/privet)')


async def on_whom(message: types.Message, state: FSMContext):
    if 'vk.com' in message.text:
        db_column = 'user_id_VK'
        link = message.text.strip('vk.com/')
        print(1)
    elif '@' in message.text:
        db_column = 'username_TG'
        link = message.text.strip('@')
        print(2)
    else:
        print(3)
        await bot.send_message(message.from_user.id, 'Введите действительную ссылку в верном формате')
        return
    async with state.proxy() as data:
        print(4)
        print(db_column, link)
        data['host_id_db'] = db.get_host_for_review(db_column, link)
    if not data.get('host_id_db'):
        print(5)
        await bot.send_message(message.from_user.id, 'Такого пользователя нет в базе данных')
    else:
        print(6)
        await bot.send_message(message.from_user.id, 'Напишите ваш отзыв')
        await FSMUsage.write_review_text.set()


async def write_review_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['review_text'] = message.text
    await FSMUsage.leave_mark.set()
    await bot.send_message(message.from_user.id, 'Поставьте оценку от 1 до 5')


async def leave_mark(message: types.Message, state: FSMContext):
    if message.text not in ['1', '2', '3', '4', '5']:
        await bot.send_message(message.from_user.id, 'Ещё раз. От одного до пяти.')
    async with state.proxy() as data:
        host_id = data.get('host_id_db')
        review = data.get('review_text')
    date = datetime.today()
    mark = message.text
    db.leave_review(host_id, message.from_user.id, review, date, mark)
    await bot.send_message(message.from_user.id, 'Ваш отзыв записан в базу данных')
    await state.finish()


def register_handlers_leave_review(dp: Dispatcher):
    dp.register_message_handler(leave_review, commands=['leavereview'], state='*')
    dp.register_message_handler(on_whom, state=FSMUsage.leave_review)
    dp.register_message_handler(write_review_text, state=FSMUsage.write_review_text)
    dp.register_message_handler(leave_mark, state=FSMUsage.leave_mark)