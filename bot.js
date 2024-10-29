const { Telegraf } = require('telegraf');
const axios = require('axios');
require('dotenv').config(); // Подключаем dotenv для работы с переменными окружения

// Инициализируем бота с вашим токеном
const bot = new Telegraf(process.env.BOT_TOKEN);

// Функция для получения троллингового сообщения от нейросети
async function getTrollingMessage(name) {
    try {
        const response = await axios.post('https://api-inference.huggingface.co/models/gpt2', {
            inputs: `Скажи что-нибудь смешное про ${name}`,
        }, {
            headers: {
                Authorization: `Bearer ${process.env.HUGGING_FACE_TOKEN}`, // Используем токен из переменной окружения
            },
        });
        return response.data[0].generated_text || "Не могу придумать что-то смешное!";
    } catch (error) {
        console.error('Ошибка при получении сообщения:', error);
        return "Что-то пошло не так!";
    }
}

// Обработка текстовых сообщений
bot.on('text', async (ctx) => {
    const name = ctx.from.first_name || 'незнакомец';
    const trollingMessage = await getTrollingMessage(name);
    ctx.reply(trollingMessage); // Отправляем троллинговое сообщение в чат
});

// Запуск бота
bot.launch()
    .then(() => {
        console.log('Бот запущен!');
    })
    .catch(err => {
        console.error('Ошибка при запуске бота:', err);
    });
