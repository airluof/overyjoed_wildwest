import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import random

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Хранение данных о пользователях в группах
group_data = {}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я бот для развлечений. Пишите мне, и я вас позабавлю!')

# Обработка текстовых сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name

    # Инициализация данных для группы, если ещё не существует
    if chat_id not in group_data:
        group_data[chat_id] = {}

    # Инициализация данных для пользователя в группе
    if user_id not in group_data[chat_id]:
        group_data[chat_id][user_id] = {'name': user_name, 'messages': []}

    # Сохраняем сообщение пользователя
    group_data[chat_id][user_id]['messages'].append(update.message.text)

    # Если у пользователя уже есть сообщения, троллим его
    if len(group_data[chat_id][user_id]['messages']) > 1:
        # Получаем случайное сообщение для троллинга
        troll_message = random.choice(group_data[chat_id][user_id]['messages'][:-1])
        await update.message.reply_text(f"Эй, {user_name}, ты когда-то говорил: '{troll_message}'? 😂")

# Основная функция
def main() -> None:
    app = ApplicationBuilder().token("8151195711:AAHusRUvtSM6CkyKtYRuFfD9Hyh_gCeZDVA").build()

    # Добавляем обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запуск бота
    app.run_polling()

if __name__ == '__main__':
    main()
