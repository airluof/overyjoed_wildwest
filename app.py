import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Получаем токен из переменной окружения
TOKEN = os.getenv("7647773708:AAE33MAv7RTc8vpcwmVUnu1j2PYxaG1-l8U")

# Проверяем, что токен установлен
if not TOKEN:
    raise ValueError("Токен бота не установлен. Пожалуйста, добавьте его в переменную окружения TELEGRAM_TOKEN.")

# Начальная команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать в мир Дикого Запада! 🌄\n"
        "Вы – отважный странник, который только что приехал в город.\n\n"
        "Используйте /profile, чтобы посмотреть свою статистику, и /buy, чтобы купить предметы."
    )

# Команда для просмотра профиля игрока
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Заглушка профиля для примера
    user_profile = {
        "уровень": 1,
        "золото": 100,
        "опыт": 0
    }
    await update.message.reply_text(
        f"📜 Ваш профиль:\n"
        f"Уровень: {user_profile['уровень']}\n"
        f"Золото: {user_profile['золото']} монет\n"
        f"Опыт: {user_profile['опыт']} XP"
    )

# Команда для покупки предметов
async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Пример предметов, которые можно купить
    items = {
        "лошадь": 50,
        "шляпа": 20,
        "револьвер": 100
    }
    item_list = "\n".join([f"{item.capitalize()}: {price} золота" for item, price in items.items()])
    await update.message.reply_text(
        f"Вы можете купить:\n{item_list}\n\n"
        "Используйте команду /buy <предмет> для покупки."
    )

# Настройка и запуск бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Регистрируем обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(CommandHandler("buy", buy))

    # Запускаем бота
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
