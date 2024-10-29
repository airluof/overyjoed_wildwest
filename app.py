import logging
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Задайте уровень логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Замените на ваш токен
TOKEN = '8151195711:AAHusRUvtSM6CkyKtYRuFfD9Hyh_gCeZDVA'
GROUP_CHAT_ID = -4576812281  # Ваш ID группы

# Словарь для хранения сообщений пользователей
user_messages = {}

# Функция для обработки текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    user_text = update.message.text

    # Сохраняем сообщение пользователя
    if user_id not in user_messages:
        user_messages[user_id] = []
    user_messages[user_id].append(user_text)

    # Генерация троллингового ответа
    response = generate_trolling_response(user_id)
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=response)

# Функция генерации смешного ответа на основе сообщений пользователя
def generate_trolling_response(user_id):
    if user_id in user_messages and user_messages[user_id]:
        # Генерируем случайный ответ, используя сохраненные сообщения
        random_message = random.choice(user_messages[user_id])
        # Составляем смешное предложение
        return f"Ты сказал: '{random_message}' 😂 Но это звучит, как будто ты наркоман! 😂"
    return "Что-то не так... 🤔"

# Функция для отправки случайных сообщений на основе пользовательских сообщений
async def random_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    for user_id in user_messages:
        if user_messages[user_id]:
            # Генерируем случайное сообщение на основе сообщений пользователя
            random_user_message = random.choice(user_messages[user_id])
            troll_message = f"Вот твое сообщение, {random_user_message} 😂"
            await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=troll_message)

async def main() -> None:
    # Создаем приложение
    application = ApplicationBuilder().token(TOKEN).build()

    # Обрабатываем текстовые сообщения
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Отправляем случайные сообщения каждые 10 секунд
    application.job_queue.run_repeating(random_message, interval=10, first=0)

    # Запускаем бота
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
