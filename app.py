import logging
import random
import sqlite3
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, JobQueue

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка базы данных
def setup_database():
    conn = sqlite3.connect('troll_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Функция для добавления сообщения в базу данных
def add_message(user_id: int, message: str):
    conn = sqlite3.connect('troll_bot.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (user_id, message) VALUES (?, ?)', (user_id, message))
    conn.commit()
    conn.close()

# Функция для генерации смешной фразы
def generate_funny_phrase(messages):
    if not messages:
        return "Нет сообщений для генерации."

    # Собираем все слова из всех сообщений
    words = []
    for message in messages:
        words.extend(message.split())

    # Генерируем случайное количество слов для смешной фразы
    random_word_count = random.randint(3, min(10, len(words)))  # Случайное количество слов от 3 до 10
    funny_phrase = ' '.join(random.sample(words, random_word_count))
    
    return funny_phrase

# Функция для получения случайного GIF
def get_random_gif():
    url = "https://api.giphy.com/v1/gifs/random?api_key=SXAPnfxLJz4dz5f2sy6h0ZpcBMjJjGef&tag=&rating=g"
    response = requests.get(url).json()
    return response['data']['images']['original']['url']

# Функция для случайного сообщения пользователю
async def random_message(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.context['chat_id']
    
    # Получаем все сообщения из базы данных
    conn = sqlite3.connect('troll_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT message FROM messages')
    messages = [row[0] for row in cursor.fetchall()]
    conn.close()

    # Генерируем смешное словосочетание
    funny_phrase = generate_funny_phrase(messages)

    await context.bot.send_message(chat_id, funny_phrase)

# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    message_text = update.message.text
    
    # Сохраняем сообщение
    add_message(user_id, message_text)

# Главная функция
if __name__ == '__main__':
    setup_database()
    
    application = ApplicationBuilder().token('8151195711:AAHusRUvtSM6CkyKtYRuFfD9Hyh_gCeZDVA').build()
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запускаем периодическую отправку сообщений в группу
    application.job_queue.run_repeating(random_message, interval=10, first=0, context={'chat_id': YOUR_CHAT_ID})

    application.run_polling()
