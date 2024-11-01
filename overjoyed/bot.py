import os
import logging
from telegram.ext import ApplicationBuilder
from overjoyed.handlers import get_update_handler, get_forward_handler, get_help_handler

# Установка уровня логирования
logging.basicConfig(level=logging.DEBUG)

async def main():
    app = ApplicationBuilder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    app.add_handler(get_update_handler())
    app.add_handler(get_forward_handler())
    app.add_handler(get_help_handler())

    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
