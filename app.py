import logging
import random
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Включение логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Список случайных троллинг-сообщений
troll_messages = [
    "О, вот снова {name}! Как твой уровень нубства?",
    "Эй, {name}, когда ты собираешься научиться играть?",
    "Что за бред ты несешь, {name}?",
    "Серьезно, {name}, ты думаешь, что это хорошая идея?",
]

# Словарь для хранения имен пользователей
usernames = {}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Я бот для троллинга. Пиши мне что-нибудь!")

# Обработка текстовых сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    username = update.message.from_user.username or update.message.from_user.first_name

    # Запоминаем имя пользователя
    usernames[user_id] = username

    # Случайное троллинг-сообщение
    if random.random() < 0.3:  # 30% вероятность ответа
        troll_message = random.choice(troll_messages).format(name=username)
        await update.message.reply_text(troll_message)
    else:
        await update.message.reply_text(f"Ты сказал: {update.message.text}")

# Основная функция
def main() -> None:
    app = ApplicationBuilder().token("8151195711:AAHusRUvtSM6CkyKtYRuFfD9Hyh_gCeZDVA").build()

    # Добавляем обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    while True:
        try:
            # Запуск бота
            app.run_polling()
        except Exception as e:
            logger.error(f"Ошибка при запуске бота: {e}")
            time.sleep(5)  # Ожидание перед повторной попыткой

if __name__ == '__main__':
    main()
