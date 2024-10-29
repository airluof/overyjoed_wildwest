import random
import requests
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from transformers import pipeline
import time

# Установите ваш токен Telegram-бота и Giphy API ключ
TELEGRAM_TOKEN = '8151195711:AAHusRUvtSM6CkyKtYRuFfD9Hyh_gCeZDVA'
GIPHY_API_KEY = 'SXAPnfxLJz4dz5f2sy6h0ZpcBMjJjGef'

# Инициализация модели
generator = pipeline('text-generation', model='gpt2')

# Список тем для сообщений
TOPICS = ["анекдоты", "приговоры", "праздники", "животные", "природа"]

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Хранит информацию о чатах, куда будет отправляться сообщение
chat_ids = set()

def send_random_message(context: CallbackContext) -> None:
    if not chat_ids:
        return  # Если нет чатов, выходим

    chat_id = random.choice(list(chat_ids))  # Выбираем случайный чат
    topic = random.choice(TOPICS)

    # Генерация сообщения с помощью модели
    message = generator(f"Напиши {topic}:", max_length=50, num_return_sequences=1)[0]['generated_text']

    # Поиск GIF по теме
    gif_url = get_random_gif(topic)

    context.bot.send_message(chat_id=chat_id, text=message)
    if gif_url:
        context.bot.send_animation(chat_id=chat_id, animation=gif_url)

def get_random_gif(topic):
    url = f"https://api.giphy.com/v1/gifs/random?api_key={GIPHY_API_KEY}&tag={topic}&rating=g"
    response = requests.get(url)
    data = response.json()
    
    if data['data']:
        return data['data']['images']['original']['url']
    return None

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Привет! Я развлекательный бот. Теперь я буду отправлять сообщения в случайное время!")
    chat_ids.add(update.message.chat_id)  # Добавляем чат в список
    context.job_queue.run_repeating(send_random_message, interval=60, first=0)  # Отправка каждые 60 секунд

def main() -> None:
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
