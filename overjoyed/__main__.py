import os
import asyncio
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Установка уровня логирования
logging.basicConfig(level=logging.DEBUG)

async def main():
    # Создание приложения Telegram
    app = ApplicationBuilder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    # Регистрация обработчиков
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск приложения
    await app.run_polling()

async def start(update, context):
    await update.message.reply_text('Привет! Я бот.')

async def handle_message(update, context):
    await update.message.reply_text('Вы написали: ' + update.message.text)

if __name__ == "__main__":
    # Получение текущего цикла событий
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
