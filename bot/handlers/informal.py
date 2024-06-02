from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters, CommandHandler

from bot.handlers.start import fresh_start
from bot.utils.utils import generic_reply, go_home, unlucky

BACK = 'Назад'
HOME = 'На головну'
INFORMAL_EDUCATION_CATEGORY, INFORMAL_COURSES, INFORMAL_RECOGNITION = range(3)


async def informal_education(update: Update, context: CallbackContext) -> int:
    buttons = [['Перезарахування курсів']]
    return await generic_reply(update, 'Оберіть категорію:', buttons, INFORMAL_EDUCATION_CATEGORY, back_button=True)


async def informal_courses(update: Update, context: CallbackContext) -> int:
    text = (
        "Чи можу я перезарахувати курси, прослухані онлайн? Так, це можливо. "
        "Кожна кафедра визначає це самостійно. Потрібно звернутись з заявою до завідувача кафедри про можливість визнання результатів неформальної освіти. "
        "Деталі доступні за [посиланням](https://www.ukma.edu.ua/index.php/about-us/sogodennya/dokumenty-naukma/doc_download/3402-polozhennia-pro-vyznannia-rezultativ-navchannia-zdobutykh-cherez-neformalnu-abo-informalnu-osvitu)."
    )
    return await generic_reply(update, text, [], INFORMAL_COURSES, back_button=True, home_button=True,
                               back_home_row=True,
                               parse_mode=ParseMode.MARKDOWN)


informal_education_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Неформальна освіта'), informal_education)],
    states={
        INFORMAL_EDUCATION_CATEGORY: [
            MessageHandler(filters.Regex('Перезарахування курсів'), informal_courses),
            MessageHandler(filters.Regex(BACK), go_home),
        ],
        INFORMAL_COURSES: [
            MessageHandler(filters.Regex(BACK), informal_education),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
    },
    fallbacks=[CommandHandler('reset', fresh_start), CommandHandler('start', fresh_start),
               MessageHandler(filters.TEXT, unlucky)],
    name='informal-education-handler',
    persistent=True,
)
