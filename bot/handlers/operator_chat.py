import asyncio
import os

from telegram import Update, Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext, MessageHandler, filters, ConversationHandler, CommandHandler

from bot.handlers.start import fresh_start
from bot.utils.config import logger
from bot.utils.utils import unlucky

IN_CONVERSATION = 1
pending_replies = {}
user_nicknames = {}
nickname_counter = 1


async def clear_pending_replies(interval: int):
    while True:
        await asyncio.sleep(interval)
        pending_replies.clear()
        logger.info('Cleared pending_replies')


async def connect_with_operator(update: Update, _: CallbackContext) -> int:
    TELEGRAM_SUPPORT_CHAT_ID = os.getenv('TELEGRAM_SUPPORT_CHAT_ID')
    chat_id = update.message.chat_id
    if int(chat_id) == int(TELEGRAM_SUPPORT_CHAT_ID):
        return
    keyboard = [
        [
            KeyboardButton('Завершити діалог'),
        ]
    ]
    keyboard_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        'Для початку діалогу з оператором, відправ повідомлення та очікуй відповіді. Для завершення діалогу натисни '
        '"Завершити діалог".',
        reply_markup=keyboard_markup)
    return IN_CONVERSATION


async def send_to_operator(update: Update, context: CallbackContext) -> int:
    global nickname_counter
    support_chat_id = os.getenv('TELEGRAM_SUPPORT_CHAT_ID')
    user = update.message.from_user
    user_id = user.id

    if user.username:
        username = f'@{user.username}'
    else:
        if user_id not in user_nicknames:
            user_nicknames[user_id] = f'User_{nickname_counter}'
            nickname_counter += 1
        username = user_nicknames[user_id]

    caption = f'{username}'

    message: Message = update.message
    message_caption = message.caption if message.caption is not None else ""

    button = InlineKeyboardButton(text='Не вибрано', callback_data='not_pressed')
    reply_markup = InlineKeyboardMarkup([[button]])

    sent_message = None
    if message.text is not None:
        sent_message = await context.bot.send_message(chat_id=support_chat_id, text=f'{caption}\n{message.text}',
                                                      reply_markup=reply_markup)
        pending_replies[sent_message.message_id] = {'chat_id': update.effective_chat.id, 'text': sent_message.text}
    elif message.photo is not None and len(message.photo) > 0:
        sent_message = await context.bot.send_photo(chat_id=support_chat_id, photo=message.photo[-1].file_id,
                                                    caption=f'{caption}\n{message_caption}', reply_markup=reply_markup)
        pending_replies[sent_message.message_id] = {'chat_id': update.effective_chat.id, 'caption': sent_message.caption}
    elif message.animation:
        sent_message = await context.bot.send_animation(chat_id=support_chat_id, animation=message.animation.file_id,
                                                        caption=f'{caption}\n', reply_markup=reply_markup)
        pending_replies[sent_message.message_id] = {'chat_id': update.effective_chat.id, 'caption': sent_message.caption}
    elif message.sticker:
        sticker = await context.bot.send_message(chat_id=support_chat_id, text=caption)
        sent_message = await context.bot.send_sticker(chat_id=support_chat_id, sticker=message.sticker.file_id,
                                                      reply_markup=reply_markup)
        pending_replies[sent_message.message_id] = {'chat_id': update.effective_chat.id}
        pending_replies[sticker.message_id] = {'chat_id': update.effective_chat.id, 'text': sticker.text}
    elif message.voice:
        sent_message = await context.bot.send_voice(chat_id=support_chat_id, voice=message.voice.file_id, caption=caption,
                                                    reply_markup=reply_markup)
        pending_replies[sent_message.message_id] = {'chat_id': update.effective_chat.id, 'caption': caption}
    elif message.video:
        sent_message = await context.bot.send_video(chat_id=support_chat_id, video=message.video.file_id, caption=caption,
                                                    reply_markup=reply_markup)
        pending_replies[sent_message.message_id] = {'chat_id': update.effective_chat.id, 'caption': caption}
    elif message.location:
        location = await context.bot.send_message(chat_id=support_chat_id, text=caption)
        sent_message = await context.bot.send_location(chat_id=support_chat_id, latitude=message.location.latitude,
                                                       longitude=message.location.longitude,
                                                       reply_markup=reply_markup)
        pending_replies[location.message_id] = {'chat_id': update.effective_chat.id, 'text': location.text}
        pending_replies[sent_message.message_id] = {'chat_id': update.effective_chat.id}
    elif message.video_note:
        video = await context.bot.send_message(chat_id=support_chat_id, text=caption)
        sent_message = await context.bot.send_video_note(chat_id=support_chat_id, video_note=message.video_note,
                                                         reply_markup=reply_markup)
        pending_replies[sent_message.message_id] = {'chat_id': update.effective_chat.id}
        pending_replies[video.message_id] = {'chat_id': update.effective_chat.id, 'text': video.text}

    elif message.document:
        sent_message = await context.bot.send_document(chat_id=support_chat_id, document=message.document.file_id,
                                                       caption=f'{caption}\n{message_caption}', reply_markup=reply_markup)
        pending_replies[sent_message.message_id] = {'chat_id': update.effective_chat.id, 'caption': sent_message.caption}

    return IN_CONVERSATION




async def go_home(update: Update, context: CallbackContext) -> int:
    user_chat_id = update.effective_chat.id
    support_chat_id = int(os.getenv('TELEGRAM_SUPPORT_CHAT_ID'))
    global pending_replies
    last_message_id = None
    last_message_text = None
    last_message_caption = None

    for message_id, info in pending_replies.items():
        if info['chat_id'] == user_chat_id:
            last_message_id = message_id
            last_message_text = info.get('text')
            last_message_caption = info.get('caption')
    if last_message_id:
        try:
            if last_message_text:
                await context.bot.edit_message_text(
                    chat_id=support_chat_id,
                    message_id=last_message_id,
                    text=last_message_text + "\n\n(ЧАТ ЗАВЕРШЕНО)"
                )
            elif last_message_caption:
                await context.bot.edit_message_caption(
                    chat_id=support_chat_id,
                    message_id=last_message_id,
                    caption=last_message_caption + "\n\n(ЧАТ ЗАВЕРШЕНО)"
                )
        except Exception as e:
            logger.error(f"Failed to edit message: {e}")

    pending_replies = {k: v for k, v in pending_replies.items() if v['chat_id'] != user_chat_id}
    from bot.handlers.start import home
    await home(update, context)
    return ConversationHandler.END




async def go_fresh_home(update: Update, context: CallbackContext) -> int:
    user_chat_id = update.effective_chat.id
    global pending_replies
    pending_replies = {k: v for k, v in pending_replies.items() if v != user_chat_id}
    await fresh_start(update, context)
    return ConversationHandler.END


async def forward_reply_to_user(update: Update, _: CallbackContext) -> None:
    message: Message = update.message
    reply_to_id = extract_reply_id(message)

    if reply_to_id:
        pending_reply = pending_replies.get(reply_to_id)
        to_chat_id = pending_reply['chat_id']
        if message.text:
            await send_message(_, to_chat_id, text=message.text)
        elif message.photo:
            await send_photo(_, to_chat_id, message)
        elif message.animation:
            await send_animation(_, to_chat_id, message)
        elif message.sticker:
            await send_sticker(_, to_chat_id, message)
        elif message.document:
            await send_document(_, to_chat_id, message)
        elif message.video:
            await send_video(_, to_chat_id, message)
        elif message.video_note:
            await send_video_note(_, to_chat_id, message)
        elif message.location:
            await send_location(_, to_chat_id, message)
        elif message.voice:
            await send_voice(_, to_chat_id, message)
        else:
            print(f'Unsupported message type: {message}')


def extract_reply_id(message):
    return message.reply_to_message.message_id if message.reply_to_message else None


async def send_message(_, chat_id, text=None):
    if text:
        await _.bot.send_message(chat_id=chat_id, text=text)


async def send_photo(_, chat_id, message):
    if len(message.photo) > 0:
        photo_file_id = message.photo[-1].file_id
        await _.bot.send_photo(chat_id=chat_id, photo=photo_file_id, caption=message.caption)


async def send_animation(_, chat_id, message):
    animation_file_id = message.animation.file_id
    await _.bot.send_animation(chat_id=chat_id, animation=animation_file_id, caption=message.caption)


async def send_sticker(_, chat_id, message):
    sticker_file_id = message.sticker.file_id
    await _.bot.send_sticker(chat_id=chat_id, sticker=sticker_file_id)


async def send_document(_, chat_id, message):
    await _.bot.send_document(chat_id=chat_id, document=message.document.file_id, caption=message.caption)


async def send_video(_, chat_id, message):
    await _.bot.send_video(chat_id=chat_id, video=message.video.file_id, caption=message.caption)


async def send_video_note(_, chat_id, message):
    await _.bot.send_video_note(chat_id=chat_id, video_note=message.video_note)


async def send_location(_, chat_id, message):
    await _.bot.send_location(chat_id=chat_id, latitude=message.location.latitude, longitude=message.location.longitude)


async def send_voice(_, chat_id, message):
    await _.bot.send_voice(chat_id=chat_id, voice=message.voice.file_id)


async def chat_id(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text=f"Chat ID: {chat_id}")


operator_chat_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('^Чат-підтримка$'), connect_with_operator)],
    states={
        IN_CONVERSATION: [
            MessageHandler(~filters.COMMAND & ~filters.Regex('Завершити діалог') & (
                    filters.TEXT | filters.PHOTO | filters.VOICE | filters.Document.ALL |
                    filters.ANIMATION | filters.Sticker.ALL | filters.VIDEO | filters.FORWARDED | filters.VIDEO | filters.LOCATION | filters.VIDEO_NOTE),
                           send_to_operator),
            MessageHandler(filters.Regex('Завершити діалог'), go_home),
        ],
    },
    fallbacks=[CommandHandler('reset', go_fresh_home), MessageHandler(filters.Regex('^/start$'), go_fresh_home),
               MessageHandler(filters.TEXT, unlucky)],
    name='operator_chat-handler',
    persistent=True,
)
reply_handler = MessageHandler(filters.REPLY, forward_reply_to_user)
