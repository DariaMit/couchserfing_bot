from aiogram import executor, types
from create_bot import dp
from handlers.find_host import find_host
from handlers.accept_reject_request import accept_reject_request
from handlers.registration import registration
from handlers.create_invit import create_invit
from handlers.start import start
from handlers.leave_review import leave_review


registration.register_handlers_registration(dp)
find_host.register_handlers_find_host(dp)
create_invit.register_handlers_create_invit(dp)
start.register_handlers_start(dp)
accept_reject_request.register_handlers_share_contacts(dp)
leave_review.register_handlers_leave_review(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)