from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Укажите токен напрямую
TOKEN = "8151195711:AAHusRUvtSM6CkyKtYRuFfD9Hyh_gCeZDVA"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать в мир Дикого Запада! 🌄\n"
        "Вы – отважный странник, который только что приехал в город.\n\n"
        "Используйте /profile, чтобы посмотреть свою статистику, и /buy, чтобы купить предметы."
    )

# Команда для профиля
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    items = {
        "лошадь": 50,
        "шляпа": 20,
        "револьвер": 100
    }
    item_list = "\n".join([f"{item.capitalize()}: {price} золота" for item, price in items.items()])
    await update.message.reply_text(f"Доступные предметы для покупки:\n{item_list}")

# Создание и запуск приложения
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("profile", profile))
app.add_handler(CommandHandler("buy", buy))

app.run_polling()
