from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from couch_bot1.create_bot import bot, db
from couch_bot1.handlers.start import FSMUsage
from .keyboards import change_invitation_rus


async def create_invitation(message: types.Message, state: FSMContext):
    if db.user_invitation_exists(message.from_user.id):
        await FSMUsage.already_host.set()
        async with state.proxy() as data:
            data['changing'] = True
        await bot.send_message(message.from_user.id, 'Вы уже создали приглашение. Хотите его изменить?',
                               reply_markup=change_invitation_rus)
    else:
        async with state.proxy() as data:
            data['changing'] = False
        await FSMUsage.host_city.set()
        await bot.send_message(message.from_user.id, 'В каком городе ты принимаешь гостей?')


async def change_invit(message: types.Message, state: FSMContext):
    if message.text in ['Да', 'Yes']:
        await FSMUsage.next()
        await bot.send_message(message.from_user.id, 'В каком городе ты принимаешь гостей?')
    elif message.text in ['Нет', 'No']:
        await state.finish()


async def host_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text
    await FSMUsage.next()
    await bot.send_message(message.from_user.id, 'Напиши текст приглашения')


async def write_invitation_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        city = data.get('city')
        if data.get('changing') == False:
            db.set_host_invitation(message.from_user.id, message.text, city)
        else:
            db.reset_host_invitation(message.from_user.id, message.text, city)
    await bot.send_message(message.from_user.id, 'Объявление создано')
    await state.finish()


def register_handlers_create_invit(dp: Dispatcher):
    dp.register_message_handler(create_invitation, commands=['createinvitation'])
    dp.register_message_handler(change_invit, state=FSMUsage.already_host)
    dp.register_message_handler(host_city, state=FSMUsage.host_city)
    dp.register_message_handler(write_invitation_text, state=FSMUsage.write_inv_text)