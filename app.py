import asyncio
import random
from collections import defaultdict
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Словарь для хранения слов пользователей
user_words = defaultdict(list)

# Список мемных фраз
meme_phrases = [
    "Когда ты {word1}, а не {word2}",
    "Ты такой {word} на самом деле!",
    "Зачем ты {word}, если можно {word2}?",
]

# Функция для обработки текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    # Запоминаем слова пользователя
    words = text.split()
    user_words[user_id].extend(words)
    print(f"Запомненные слова для пользователя {user_id}: {user_words[user_id]}")

# Функция для отправки случайных сообщений
async def send_random_messages(context: ContextTypes.DEFAULT_TYPE):
    for user_id, words in user_words.items():
        if words:
            # Генерация случайной мемной фразы
            selected_phrase = random.choice(meme_phrases)
            selected_words = random.sample(words, min(2, len(words)))  # Берем случайные слова

            # Подстановка слов в мемную фразу
            message = selected_phrase.format(word1=selected_words[0], word2=selected_words[1] if len(selected_words) > 1 else selected_words[0])
            await context.bot.send_message(chat_id=user_id, text=message)
            print(f"Отправлено сообщение пользователю {user_id}: {message}")

# Основная функция
async def main():
    app = ApplicationBuilder().token("8151195711:AAHusRUvtSM6CkyKtYRuFfD9Hyh_gCeZDVA").build()

    app.add_handler(CommandHandler("start", lambda update, context: context.bot.send_message(chat_id=update.effective_chat.id, text="Я бот, запоминаю ваши слова!")))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем JobQueue для отправки случайных сообщений
    job_queue = app.job_queue
    job_queue.run_repeating(send_random_messages, interval=10, first=0)

    print("Бот запущен и ждет сообщений...")
    await app.initialize()  # Явно инициализируем приложение
    await app.start()  # Запускаем приложение
    await app.updater.start_polling()  # Запускаем polling
    await app.idle()  # Ожидаем завершения работы приложения

if __name__ == "__main__":
    asyncio.run(main())  # Используем asyncio.run() для запуска основной функции
