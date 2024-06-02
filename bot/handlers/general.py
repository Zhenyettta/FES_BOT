from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, MessageHandler, filters

from bot.handlers.start import fresh_start
from bot.utils.utils import generic_reply, go_home, unlucky

BACK = 'Назад'
HOME = 'На головну'
GENERAL_INFO_CATEGORY, CAMPUS_MAP, LIBRARIES, REPOSITORY, DORMITORIES, SCHOLARSHIPS, CALENDAR, RANKINGS = range(8)


async def general_info(update: Update, context: CallbackContext) -> int:
    buttons = [['Схема університетського містечка', 'Бібліотеки НаУКМА'],
               ['Репозиторій НаУКМА', 'Гуртожитки'],
               ['Стипендії та відзнаки', 'Календарний графік'],
               ['Рейтинг стипендій']]
    return await generic_reply(update, 'Оберіть категорію:', buttons, GENERAL_INFO_CATEGORY, back_button=True)


async def campus_map(update: Update, context: CallbackContext) -> int:
    text = (
        "Для перегляду схеми університетського містечка, перейдіть за [посиланням](https://www.ukma.edu.ua/index.php/about-us/istoriya-akademiji/images/docs/plan/polozhenya/264_01%2007%2015%20pidgotov%20do%20vstupu.pdf)."
    )
    return await generic_reply(update, text, [], CAMPUS_MAP, back_button=True, home_button=True, back_home_row=True,
                               parse_mode=ParseMode.MARKDOWN)


async def libraries(update: Update, context: CallbackContext) -> int:
    text = (
        "Для перегляду інформації про бібліотеки НаУКМА, перейдіть за [посиланням](https://library.ukma.edu.ua)."
    )
    return await generic_reply(update, text, [], LIBRARIES, back_button=True, home_button=True, back_home_row=True,
                               parse_mode=ParseMode.MARKDOWN)


async def repository(update: Update, context: CallbackContext) -> int:
    text = (
        "Для перегляду репозиторію НаУКМА, перейдіть за [посиланням](https://ekmair.ukma.edu.ua/home)."
    )
    return await generic_reply(update, text, [], REPOSITORY, back_button=True, home_button=True, back_home_row=True,
                               parse_mode=ParseMode.MARKDOWN)


async def dormitories(update: Update, context: CallbackContext) -> int:
    text = (
        "Для перегляду інформації про гуртожитки, перейдіть за [посиланням](https://web.ukma.edu.ua/index.php/uk/students/dormitories)."
    )
    return await generic_reply(update, text, [], DORMITORIES, back_button=True, home_button=True, back_home_row=True,
                               parse_mode=ParseMode.MARKDOWN)


async def scholarships(update: Update, context: CallbackContext) -> int:
    text = (
        "Для перегляду інформації про стипендії та відзнаки студентам НаУКМА, перейдіть за [посиланням](https://www.ukma.edu.ua/index.php/about-us/spilnoti/students-life/stypendii-ta-vidznaky)."
    )
    return await generic_reply(update, text, [], SCHOLARSHIPS, back_button=True, home_button=True, back_home_row=True,
                               parse_mode=ParseMode.MARKDOWN)


async def calendar(update: Update, context: CallbackContext) -> int:
    text = (
        "Для перегляду календарного графіку освітнього процесу"
    )
    return await generic_reply(update, text, [], CALENDAR, back_button=True, home_button=True, back_home_row=True)


async def rankings(update: Update, context: CallbackContext) -> int:
    text = (
        "Для перегляду рейтингу стипендій, перейдіть за [посиланням](https://www.ukma.edu.ua/index.php/about-us/sogodennya/dokumenty-naukma/cat_view/1-dokumenty-naukma/12-normatyvna-baza-naukma/21-stypendialne-zabezpechennia-studentiv-aspirantiv-hrantovi-ta-konkursni-prohramy/61-reitynhy-uspishnosti-studentiv)."
    )
    return await generic_reply(update, text, [], RANKINGS, back_button=True, home_button=True, back_home_row=True,
                               parse_mode=ParseMode.MARKDOWN)


general_info_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Загальна інформація'), general_info)],
    states={
        GENERAL_INFO_CATEGORY: [
            MessageHandler(filters.Regex('Схема університетського містечка'), campus_map),
            MessageHandler(filters.Regex('Бібліотеки НаУКМА'), libraries),
            MessageHandler(filters.Regex('Репозиторій НаУКМА'), repository),
            MessageHandler(filters.Regex('Гуртожитки'), dormitories),
            MessageHandler(filters.Regex('Стипендії та відзнаки'), scholarships),
            MessageHandler(filters.Regex('Календарний графік'), calendar),
            MessageHandler(filters.Regex('Рейтинг стипендій'), rankings),
            MessageHandler(filters.Regex(BACK), go_home),
        ],
        CAMPUS_MAP: [
            MessageHandler(filters.Regex(BACK), general_info),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        LIBRARIES: [
            MessageHandler(filters.Regex(BACK), general_info),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        REPOSITORY: [
            MessageHandler(filters.Regex(BACK), general_info),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        DORMITORIES: [
            MessageHandler(filters.Regex(BACK), general_info),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        SCHOLARSHIPS: [
            MessageHandler(filters.Regex(BACK), general_info),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        CALENDAR: [
            MessageHandler(filters.Regex(BACK), general_info),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        RANKINGS: [
            MessageHandler(filters.Regex(BACK), general_info),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
    },
    fallbacks=[CommandHandler('reset', fresh_start), CommandHandler('start', fresh_start),
               MessageHandler(filters.TEXT, unlucky)],
    name='general-info-handler',
    persistent=True,
)
