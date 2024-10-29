import random
import logging
from collections import defaultdict
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Словарь для хранения слов пользователей
user_words = defaultdict(list)

# Функция для генерации мемных словосочетаний
def generate_meme(user_id):
    words = user_words[user_id]
    if len(words) < 2:
        return None
    return f"{random.choice(words)} {random.choice(words)}"

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    # Запоминаем слова пользователя
    words = text.split()
    user_words[user_id].extend(words)

    # Генерируем мемное словосочетание
    meme = generate_meme(user_id)
    if meme:
        await update.message.reply_text(meme)

# Основная функция
async def main():
    # Создание приложения
    app = ApplicationBuilder().token("8151195711:AAHusRUvtSM6CkyKtYRuFfD9Hyh_gCeZDVA").build()

    # Добавление обработчиков
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
