import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Получение токена из переменных окружения
TOKEN = os.getenv("7647773708:AAHarSrLNkpcnGIAyr2GJykhd1rqNtiY5JU")

# Приветственное сообщение
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = (
        "🤠 Добро пожаловать в мир Дикого Запада!\n"
        "Здесь вы можете:\n"
        "- Начать приключения\n"
        "- Покупать предметы\n"
        "- Сражаться с другими игроками\n"
        "- Участвовать в случайных событиях\n"
        "Используйте команды, чтобы узнать больше!\n"
        "Команды:\n"
        "/start - Начать игру\n"
        "/help - Получить помощь\n"
        "/stats - Посмотреть свою статистику\n"
        "/shop - Открыть магазин"
    )
    await update.message.reply_text(welcome_message)

# Помощь
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_message = (
        "Вот что вы можете сделать:\n"
        "/start - Начать игру\n"
        "/help - Получить помощь\n"
        "/stats - Посмотреть свою статистику\n"
        "/shop - Открыть магазин"
    )
    await update.message.reply_text(help_message)

# Статистика
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Здесь вы можете добавить логику для отображения статистики игрока
    stats_message = "📊 Ваша статистика:\n- Уровень: 1\n- Валюта: 100\n- Здоровье: 100"
    await update.message.reply_text(stats_message)

# Магазин
async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Здесь вы можете добавить логику для отображения товаров в магазине
    shop_message = (
        "🏪 Добро пожаловать в магазин! Вы можете купить:\n"
        "- Револьвер - 50 монет\n"
        "- Лошадь - 100 монет"
    )
    await update.message.reply_text(shop_message)

if __name__ == '__main__':
    # Создание приложения бота
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Регистрация команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("shop", shop))

    # Запуск бота
    app.run_polling()
