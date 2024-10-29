import logging
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Включите логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Храните сообщения пользователей
user_messages = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Бот готов к работе!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global user_messages
    user_messages.append(update.message.text)  # Сохраняем сообщение пользователя
    await update.message.reply_text("Сообщение сохранено!")

async def send_random_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    global user_messages
    if user_messages:
        message = random.choice(user_messages)  # Выбираем случайное сообщение
        await context.bot.send_message(chat_id=context.job.context['chat_id'], text=message)

async def main() -> None:
    application = ApplicationBuilder().token("8151195711:AAHusRUvtSM6CkyKtYRuFfD9Hyh_gCeZDVA").build()

    # Команды
    application.add_handler(CommandHandler("start", start))

    # Обработка сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск периодической задачи
    job_queue = application.job_queue
    chat_id = -4576812281  # Замените на ваш chat_id для группы
    job_queue.run_repeating(send_random_message, interval=10, first=0, context={'chat_id': chat_id})

    # Запуск бота
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
