import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from transformers import pipeline

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка модели для генерации ответов
model_name = "microsoft/DialoGPT-medium"
generator = pipeline('text-generation', model=model_name)

# Команда /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я твой тролль-бот. Начинай говорить, и я дам тебе ответ!')

# Обработка текстовых сообщений
def troll(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    # Генерация ответа
    response = generator(user_message, max_length=50, num_return_sequences=1)
    troll_response = response[0]['generated_text']
    update.message.reply_text(troll_response)

def main() -> None:
    # Вставьте ваш токен
    updater = Updater("8151195711:AAHusRUvtSM6CkyKtYRuFfD9Hyh_gCeZDVA")

    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрация обработчиков команд и сообщений
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, troll))

    # Запуск бота
    updater.start_polling()

    # Запуск бота до завершения работы
    updater.idle()

if __name__ == '__main__':
    main()
