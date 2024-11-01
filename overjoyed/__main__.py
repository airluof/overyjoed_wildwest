import logging
import asyncio
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from troll_bot.handlers import get_update_handler, get_forward_handler, get_help_handler

# Загружаем переменные окружения из .env файла
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

async def main():
    """Основная функция для запуска бота."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        log.error("Токен бота не найден в переменных окружения.")
        return

    app = ApplicationBuilder().token(token).build()

    # Добавление обработчиков
    app.add_handler(get_update_handler())
    app.add_handler(get_forward_handler())
    app.add_handler(get_help_handler())

    # Запуск бота
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
