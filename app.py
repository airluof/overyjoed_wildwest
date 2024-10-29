import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from huggingface_hub import InferenceApi

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализируем Hugging Face API
hf_token = "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"  # Замените на ваш токен Hugging Face
api = InferenceApi(repo_id="gpt2", token=hf_token)  # Используем модель GPT-2

# Функция для генерации ответа
async def generate_response(user_message):
    try:
        response = api(inputs=user_message)
        logger.info(f"Response from API: {response}")  # Логируем ответ от API

        # Проверяем, что ответ имеет ожидаемую структуру
        if isinstance(response, list) and len(response) > 0 and 'generated_text' in response[0]:
            return response[0]['generated_text']
        else:
            logger.error(f"Unexpected response structure: {response}")
            return "Извините, я не понял."
    except Exception as e:
        logger.error(f"Error while generating response: {e}")
        return "Извините, произошла ошибка."

# Обработка текстовых сообщений
async def troll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    # Проверяем, чтобы бот не отвечал сам себе
    if update.message.from_user.id != context.bot.id:
        troll_response = await generate_response(user_message)
        await update.message.reply_text(troll_response)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я твой тролль-бот. Начинай говорить, и я дам тебе ответ!')

def main() -> None:
    # Вставьте токен вашего Telegram бота
    app = Application.builder().token("8151195711:AAHusRUvtSM6CkyKtYRuFfD9Hyh_gCeZDVA").build()

    # Регистрация обработчика для команды /start
    app.add_handler(CommandHandler("start", start))
    # Регистрация обработчика для всех текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, troll))

    # Запуск бота
    app.run_polling()

if __name__ == '__main__':
    main()
