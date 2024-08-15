from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, MessageHandler, filters

from bot.handlers.start import fresh_start
from bot.utils.utils import generic_reply, go_home, unlucky

BACK = 'Назад'
HOME = 'На головну'
USEFUL_LINKS, STUDENT_DEPARTMENT, STUDENT_SELF_GOVERNANCE, INTERNATIONAL_DEPARTMENT = range(4)
CAREER_CENTER, ALUMNI_DEPARTMENT, SOCIAL_ADAPTATION_CENTER = range(4, 7)


# Useful Links Handlers
async def useful_links(update: Update, context: CallbackContext) -> int:
    buttons = [['Відділ по роботі зі студентами', 'Студентське самоврядування'],
               ['Відділ міжнародного співробітництва НаУКМА', 'Центр кар’єри та працевлаштування випускників НаУКМА'],
               ['Відділ по роботі з випускниками НаУКМА', 'Центр соціально-психологічної адаптації']]
    return await generic_reply(update, 'Оберіть категорію корисних посилань:', buttons, USEFUL_LINKS, back_button=True)


async def student_department(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, '[Відділ по роботі зі студентами](https://www.ukma.edu.ua/index.php/about-us/spilnoti/students-life/about)', [], STUDENT_DEPARTMENT, back_button=True, home_button=True, parse_mode=ParseMode.MARKDOWN, back_home_row=True)


async def student_self_governance(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, '[Студентське самоврядування]https://www.ukma.edu.ua/index.php/about-us/spilnoti/students-life/studentske-samovriaduvannia)', [], STUDENT_SELF_GOVERNANCE, back_button=True, home_button=True, parse_mode=ParseMode.MARKDOWN, back_home_row=True)


async def international_department(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, '[Відділ міжнародного співробітництва НаУКМА](https://dfc.ukma.edu.ua/)', [], INTERNATIONAL_DEPARTMENT, back_button=True, home_button=True, parse_mode=ParseMode.MARKDOWN, back_home_row=True)


async def career_center(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, '[Центр кар’єри та працевлаштування випускників НаУКМА](https://www.facebook.com/JCCofNaUKMA)', [], CAREER_CENTER, back_button=True, home_button=True, parse_mode=ParseMode.MARKDOWN, back_home_row=True)


async def alumni_department(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, '[Відділ по роботі з випускниками НаУКМА](https://alumni.ukma.edu.ua/)', [], ALUMNI_DEPARTMENT, back_button=True, home_button=True, parse_mode=ParseMode.MARKDOWN, back_home_row=True)


async def social_adaptation_center(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, '[Центр соціально-психологічної адаптації](https://www.ukma.edu.ua/index.php/science/tsentri-ta-laboratoriji/cmhpss/pro-nas)', [], SOCIAL_ADAPTATION_CENTER, back_button=True, home_button=True, parse_mode=ParseMode.MARKDOWN, back_home_row=True)


# Conversation Handler
useful_links_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Корисні посилання'), useful_links)],
    states={
        USEFUL_LINKS: [
            MessageHandler(filters.Regex('Відділ по роботі зі студентами'), student_department),
            MessageHandler(filters.Regex('Студентське самоврядування'), student_self_governance),
            MessageHandler(filters.Regex('Відділ міжнародного співробітництва НаУКМА'), international_department),
            MessageHandler(filters.Regex('Центр кар’єри та працевлаштування випускників НаУКМА'), career_center),
            MessageHandler(filters.Regex('Відділ по роботі з випускниками НаУКМА'), alumni_department),
            MessageHandler(filters.Regex('Центр соціально-психологічної адаптації'), social_adaptation_center),
            MessageHandler(filters.Regex(BACK), go_home),
        ],
        STUDENT_DEPARTMENT: [
            MessageHandler(filters.Regex(BACK), useful_links),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        STUDENT_SELF_GOVERNANCE: [
            MessageHandler(filters.Regex(BACK), useful_links),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        INTERNATIONAL_DEPARTMENT: [
            MessageHandler(filters.Regex(BACK), useful_links),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        CAREER_CENTER: [
            MessageHandler(filters.Regex(BACK), useful_links),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        ALUMNI_DEPARTMENT: [
            MessageHandler(filters.Regex(BACK), useful_links),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        SOCIAL_ADAPTATION_CENTER: [
            MessageHandler(filters.Regex(BACK), useful_links),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
    },
    fallbacks=[CommandHandler('reset', fresh_start), CommandHandler('start', fresh_start),
               MessageHandler(filters.TEXT, unlucky)],
    name='useful-links-handler',
    persistent=True,
)
