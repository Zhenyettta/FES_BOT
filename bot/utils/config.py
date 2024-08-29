import logging
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext


def load_env():
    dir_of_script = Path(__file__).parent
    env_path = dir_of_script.parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)


logging.basicConfig(filename='Logs.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def chat_id(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text=f"Chat ID: {chat_id}")

def run_healthcheck_server():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()
