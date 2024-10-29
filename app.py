import random
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import asyncio

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Хранение сообщений
messages = []

# Примеры остроумных ответов
def generate_response(user_message):
    """Генерирует остроумный ответ на основе пользовательского сообщения."""
    responses = [
        f"{user_message.split(':')[0]}, я тоже в тебя верю! Мы сможем это сделать вместе!",
        f"'{user_message}'? А как же это 'привет' для начала?",
        f"Ого, '{user_message}' - звучит как приглашение на дискуссию!",
        f"Если '{user_message}' - это ваше приветствие, то мне страшно думать о следующем сообщении!",
    ]
    return random.choice(responses)

async def send_funny_message(context: ContextTypes.DEFAULT_TYPE):
    """Отправляет случайное остроумное сообщение в чат, основываясь на запомненных сообщениях."""
    chat_id = context.job.context
    if chat_id is not None and messages:
        user_message = random.choice(messages)
        response = generate_response(user_message)
        await context.bot.send_message(chat_id=chat_id, text=response)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений."""
    text = update.message.text
    messages.append(text)  # Запоминаем сообщение
    logging.info(f"Запомнено сообщение: {text}")

async def main():
    """Запуск бота."""
    application = ApplicationBuilder().token("8151195711:AAHusRUvtSM6CkyKtYRuFfD9Hyh_gCeZDVA").build()

    # Обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    # Получаем chat_id из первого сообщения
    async def set_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Устанавливает chat_id для JobQueue."""
        context.job_queue.run_repeating(send_funny_message, interval=300, first=0, context=update.message.chat.id)

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, set_chat_id, run_async=True))

    # Запуск бота
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
