import asyncio
import logging
import os


from telegram import Update
from telegram.ext import Application, CallbackQueryHandler, PicklePersistence, CommandHandler

from bot.handlers.contacts import contacts_handler
from bot.handlers.general import general_info_handler
from bot.handlers.informal import informal_education_handler
from bot.handlers.mobility import mobility_handler
from bot.handlers.start import start_handler
from bot.handlers.study_process import learning_process_handler
from bot.handlers.usefull_links import useful_links_handler
from bot.utils.config import load_env

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
if __name__ == '__main__':
    load_env()
    persistence = PicklePersistence(filepath="bot.pickle")
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).persistence(
        persistence=persistence).concurrent_updates(True).build()

    application.add_handler(contacts_handler)
    application.add_handler(mobility_handler)
    application.add_handler(general_info_handler)
    application.add_handler(informal_education_handler)
    application.add_handler(learning_process_handler)
    application.add_handler(useful_links_handler)


    application.add_handler(start_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)
