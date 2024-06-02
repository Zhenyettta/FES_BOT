from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, MessageHandler, filters

from bot.handlers.start import fresh_start
from bot.utils.fields import *
from bot.utils.utils import generic_reply, go_home, unlucky

BACK = 'Назад'
HOME = 'На головну'
CONTACTS_CATEGORY, DEAN_CONTACTS, METHODISTS_CATEGORY, SVK_OR_HLIB_CONTACTS, DEPARTMENT_CONTACTS = range(5)


async def contacts(update: Update, context: CallbackContext) -> int:
    buttons = [['Контакти деканату', 'Контакти методистів кафедр'], ['Контакти СВК', 'Відділ у справах студентства']]
    return await generic_reply(update, 'Оберіть категорію:', buttons, CONTACTS_CATEGORY, back_button=True)


async def dean(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, CONTACTS_DEAN_TEXT, [], DEAN_CONTACTS, back_button=True, home_button=True,
                               back_home_row=True, parse_mode=ParseMode.MARKDOWN)


async def methodists(update: Update, context: CallbackContext) -> int:
    buttons = [['Фінанси', 'ЕТ', 'МУБ']]
    return await generic_reply(update, 'Оберіть кафедру:', buttons, METHODISTS_CATEGORY, back_button=True,
                               home_button=True)


async def svk(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, CONTACTS_SVK_TEXT, [], SVK_OR_HLIB_CONTACTS, back_button=True, home_button=True,
                               back_home_row=True)


async def hlib(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, CONTACTS_HLIB_TEXT, [], SVK_OR_HLIB_CONTACTS, back_button=True, home_button=True,
                               back_home_row=True)


async def finance(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, CONTACTS_FINANCE_TEXT, [], DEPARTMENT_CONTACTS, back_button=True,
                               home_button=True,
                               back_home_row=True)


async def et(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, CONTACTS_ET_TEXT, [], DEPARTMENT_CONTACTS, back_button=True, home_button=True,
                               back_home_row=True)


async def myb(update: Update, context: CallbackContext) -> int:
    return await generic_reply(update, CONTACTS_MYB_TEXT, [], DEPARTMENT_CONTACTS, back_button=True, home_button=True,
                               back_home_row=True)


contacts_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('Контакти'), contacts)],
    states={
        CONTACTS_CATEGORY: [
            MessageHandler(filters.Regex('Контакти деканату'), dean),
            MessageHandler(filters.Regex('Контакти методистів кафедр'), methodists),
            MessageHandler(filters.Regex('Контакти СВК'), svk),
            MessageHandler(filters.Regex('Відділ у справах студентства'), hlib),
            MessageHandler(filters.Regex(BACK), go_home),
        ],
        METHODISTS_CATEGORY: [
            MessageHandler(filters.Regex('Фінанси'), finance),
            MessageHandler(filters.Regex('ЕТ'), et),
            MessageHandler(filters.Regex('МУБ'), myb),
            MessageHandler(filters.Regex(BACK), contacts),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        DEAN_CONTACTS: [
            MessageHandler(filters.Regex(BACK), contacts),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        DEPARTMENT_CONTACTS: [
            MessageHandler(filters.Regex(BACK), methodists),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
        SVK_OR_HLIB_CONTACTS: [
            MessageHandler(filters.Regex(BACK), contacts),
            MessageHandler(filters.Regex(HOME), go_home),
        ],
    },
    fallbacks=[CommandHandler('reset', fresh_start), CommandHandler('start', fresh_start),
               MessageHandler(filters.TEXT, unlucky)],
    name='contacts-handler',
    persistent=True,
)
