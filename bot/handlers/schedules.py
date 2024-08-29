from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters, CommandHandler

from bot.handlers.start import fresh_start
from bot.utils.utils import generic_reply, go_home, unlucky

BACK = 'Назад'
HOME = 'На головну'

SCHEDULES, CLASS_SCHEDULE, EXAM_SCHEDULE = range(3)


async def schedules(update: Update, context: CallbackContext) -> int:
    buttons = [['Розклад занять', 'Розклад сесії']]
    return await generic_reply(update, 'Оберіть розклад:', buttons, SCHEDULES, back_button=True)


async def class_schedule(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, 'Розклад занять: [посилання](https://my.ukma.edu.ua/schedule)', [],
                               CLASS_SCHEDULE, back_button=True, home_button=True, parse_mode=ParseMode.MARKDOWN,
                               back_home_row=True)


async def exam_schedule(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update,
                               'Розклад сесії: [посилання](https://www.ukma.edu.ua/index.php/about-us/sogodennya/dokumenty-naukma/cat_view/1-dokumenty-naukma/30-rizne)',
                               [], EXAM_SCHEDULE,
                               back_button=True, home_button=True, parse_mode=ParseMode.MARKDOWN,
                               back_home_row=True)


# Conversation Handler
schedules_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Розклад'), schedules)],
    states={
        SCHEDULES: [
            MessageHandler(filters.Regex('Розклад занять'), class_schedule),
            MessageHandler(filters.Regex('Розклад сесії'), exam_schedule),
            MessageHandler(filters.Regex(BACK), go_home),
        ],
        CLASS_SCHEDULE: [
            MessageHandler(filters.Regex(BACK), schedules),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        EXAM_SCHEDULE: [
            MessageHandler(filters.Regex(BACK), schedules),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
    },
    fallbacks=[CommandHandler('reset', fresh_start), CommandHandler('start', fresh_start),
               MessageHandler(filters.TEXT, unlucky)],
    name='schedules_handler',
    persistent=True,
)
