import logging
import random
import sqlite3
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка базы данных
def setup_database():
    conn = sqlite3.connect('troll_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            word TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Функция для добавления слова в базу данных
def add_word(user_id: int, word: str):
    conn = sqlite3.connect('troll_bot.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO words (user_id, word) VALUES (?, ?)', (user_id, word))
    conn.commit()
    conn.close()

# Функция для генерации ответа на основе слов пользователей
def generate_response(user_id):
    conn = sqlite3.connect('troll_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT word FROM words WHERE user_id = ?', (user_id,))
    words = [row[0] for row in cursor.fetchall()]
    conn.close()

    if not words:
        return "У тебя пока нет слов. Напиши что-нибудь!"

    # Генерируем случайное количество слов для ответа
    random_word_count = random.randint(1, min(5, len(words)))  # Случайное количество слов от 1 до 5
    response = ' '.join(random.sample(words, random_word_count))
    
    return response

# Функция для получения случайного GIF
def get_random_gif():
    url = "https://api.giphy.com/v1/gifs/random?api_key=SXAPnfxLJz4dz5f2sy6h0ZpcBMjJjGef&tag=&rating=g"
    response = requests.get(url).json()
    return response['data']['images']['original']['url']

# Функция для случайного сообщения пользователю
async def random_message(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.context['chat_id']
    gif_url = get_random_gif()
    await context.bot.send_message(chat_id, "Смешное сообщение от бота!")
    await context.bot.send_animation(chat_id, gif_url)

# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    message_text = update.message.text
    
    # Сохраняем каждое слово из сообщения
    for word in message_text.split():
        add_word(user_id, word)

    # Генерируем ответ
    response = generate_response(user_id)
    await update.message.reply_text(response)

    # Отправляем случайный GIF
    gif_url = get_random_gif()
    await update.message.reply_animation(gif_url)

# Главная функция
if __name__ == '__main__':
    setup_database()
    
    application = ApplicationBuilder().token('8151195711:AAHusRUvtSM6CkyKtYRuFfD9Hyh_gCeZDVA').build()
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запускаем периодическую отправку сообщений в группу
    application.job_queue.run_repeating(random_message, interval=10, first=0, context={'chat_id': YOUR_CHAT_ID})

    application.run_polling()
