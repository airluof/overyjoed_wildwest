import logging
import random
import asyncio
from collections import defaultdict
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Хранилище фраз пользователей
user_phrases = defaultdict(list)

# Функция для генерации мемных фраз
def generate_meme(user_id):
    if user_phrases[user_id]:
        return random.choice(user_phrases[user_id])
    return None

# Обработчик сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    # Сохраняем сообщение пользователя
    user_phrases[user_id].append(text)

    # Генерируем мемную фразу
    meme = generate_meme(user_id)
    if meme:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=meme)

# Функция для периодической отправки случайных сообщений
async def send_random_messages(context):
    job_context = context.job.context
    if user_phrases:
        user_id = random.choice(list(user_phrases.keys()))
        meme = generate_meme(user_id)
        if meme:
            await context.bot.send_message(chat_id=job_context, text=meme)

# Команда для старта бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Бот запущен! Начни общаться!')

# Основная функция
async def main():
    app = ApplicationBuilder().token("8151195711:AAHusRUvtSM6CkyKtYRuFfD9Hyh_gCeZDVA").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Добавление задачи на отправку случайных сообщений
    job_queue = app.job_queue
    job_queue.run_repeating(send_random_messages, interval=10, first=0, context=update.effective_chat.id)

    await app.run_polling()

if __name__ == '__main__':
    # Получаем текущий цикл событий и запускаем основную функцию
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
