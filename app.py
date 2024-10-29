from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, JobQueue
import random

# Глобальная переменная для хранения сообщений
user_messages = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Бот запущен!")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Сохраняем сообщение пользователя
    user_messages.append(update.message.text)

async def send_random_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = context.job.data['chat_id']  # Получаем chat_id из data
    if user_messages:
        random_message = random.choice(user_messages)
        await context.bot.send_message(chat_id=chat_id, text=random_message)

async def main() -> None:
    application = ApplicationBuilder().token('8151195711:AAHusRUvtSM6CkyKtYRuFfD9Hyh_gCeZDVA').build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    # Получаем JobQueue
    job_queue = application.job_queue

    # Добавляем задачу, чтобы бот отправлял сообщения через определенный интервал
    chat_id = 'YOUR_GROUP_CHAT_ID'  # Укажите ID группы здесь
    job_queue.run_repeating(send_random_message, interval=10, first=0, data={'chat_id': chat_id})

    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
