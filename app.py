import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from huggingface_hub import InferenceApi

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализируем Hugging Face API
hf_token = "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"  # Замените на ваш токен
api = InferenceApi(repo_id="gpt2", token=hf_token)  # Подключаемся к модели GPT-2

# Команда /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я твой тролль-бот. Начинай говорить, и я дам тебе ответ!')

# Функция для генерации ответа
def generate_response(user_message):
    response = api(inputs=user_message)
    return response[0]['generated_text'] if 'generated_text' in response[0] else "Извините, я не понял."

# Обработка текстовых сообщений
def troll(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    # Генерация ответа через API
    troll_response = generate_response(user_message)
    update.message.reply_text(troll_response)

def main() -> None:
    # Вставьте ваш токен Telegram бота
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
