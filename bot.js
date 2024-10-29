const { Telegraf } = require('telegraf');
const axios = require('axios');
require('dotenv').config(); // Подключаем dotenv для работы с переменными окружения

// Инициализируем бота с вашим токеном
const bot = new Telegraf(process.env.BOT_TOKEN);

// Функция для получения троллингового сообщения от нейросети
async function getTrollingMessage(name) {
    try {
        const response = await axios.post('https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B', {
            inputs: `Напиши шутку о ${name}`, // Используем модель GPT-Neo
        }, {
            headers: {
                Authorization: `Bearer ${process.env.HUGGING_FACE_TOKEN}`, // Используем токен из переменной окружения
            },
        });

        // Логируем ответ от модели
        console.log('Ответ от модели:', response.data);

        // Проверяем корректность ответа
        if (response.data && response.data[0] && response.data[0].generated_text) {
            return response.data[0].generated_text;
        } else {
            return "Не могу придумать что-то смешное!";
        }
    } catch (error) {
        console.error('Ошибка при получении сообщения:', error);
        return "Что-то пошло не так!";
    }
}

// Обработка текстовых сообщений
bot.on('text', async (ctx) => {
    try {
        const name = ctx.from.first_name || 'незнакомец';
        const trollingMessage = await getTrollingMessage(name);
        ctx.reply(trollingMessage); // Отправляем троллинговое сообщение в чат
    } catch (error) {
        console.error('Ошибка при обработке сообщения:', error);
        ctx.reply('Произошла ошибка, попробуйте еще раз.');
    }
});

// Запуск бота
bot.launch()
    .then(() => {
        console.log('Бот запущен!');
    })
    .catch(err => {
        console.error('Ошибка при запуске бота:', err);
    });
