import logging
import random
import datetime

from overjoyed.audio import send_audio
from overjoyed.gif import send_gif
from overjoyed.database import search_messages
from overjoyed.utils import return_true_by_percentage, random_item

log = logging.getLogger(__name__)

def should_reply():
    """Определяет, следует ли боту отвечать на сообщение."""
    return return_true_by_percentage(5)

def get_random_message_word(message_received):
    """Возвращает случайное слово из текста сообщения."""
    message_words = message_received.text.split()
    log.debug('Message words: %s', message_words)
    random_word = random_item(message_words)
    return random_word

def get_reply_message(words_list, chat_id):
    """Возвращает сообщение-ответ на основе списка слов."""
    possible_messages = search_messages(words_list, chat_id)
    possible_messages = remove_last_if_young(possible_messages)

    if not possible_messages:
        log.debug('No possible messages to reply.')
        return None

    reply_message = random_item(possible_messages)
    log.debug('Reply message: %s', reply_message)
    return reply_message

def remove_last_if_young(messages):
    """Удаляет последнее сообщение, если оно было отправлено недавно."""
    if not messages:
        return []

    last_message_datetime = datetime.datetime.fromtimestamp(messages[-1]['date'])
    last_message_ago = datetime.datetime.now() - last_message_datetime

    log.debug('Seconds from last message: %s', last_message_ago.total_seconds())
    if last_message_ago.total_seconds() < 2:
        log.debug('Removing last message from reply, too young')
        return messages[:-1]

    return messages

def get_reply_type():
    """Определяет тип ответа: текст, GIF или аудио."""
    case = random.randint(1, 100)
    if case <= 80:
        return 'text'
    elif case <= 90:
        return 'gif'
    else:
        return 'audio'

async def reply_text_message(bot, chat_id, reply_message):
    """Отправляет текстовое сообщение."""
    if 'chat' not in reply_message or 'id' not in reply_message['chat'] or 'message_id' not in reply_message:
        log.error("reply_message lacks necessary data: %s", reply_message)
        return

    try:
        await bot.forwardMessage(
            chat_id=chat_id,
            from_chat_id=reply_message['chat']['id'],
            message_id=reply_message['message_id']
        )
        log.info("Message forwarded successfully.")
    except Exception as e:
        log.error(f"Failed to forward message: {e}")

async def reply_audio_message(bot, chat_id, reply_message):
    """Отправляет аудиосообщение."""
    try:
        await send_audio(bot, chat_id, reply_message['text'])
        log.info("Audio message sent successfully.")
    except Exception as e:
        log.error(f"Failed to send audio message: {e}")

async def reply_gif_message(bot, chat_id, reply_word):
    """Отправляет GIF-сообщение."""
    try:
        await send_gif(bot, chat_id, reply_word)
        log.info("GIF message sent successfully.")
    except Exception as e:
        log.error(f"Failed to send GIF message: {e}")
