import os
import telebot
from utils import get_daily_horoscope

# Получаем токен из переменной окружения
BOT_TOKEN = os.environ.get('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN не установлена")

bot = telebot.TeleBot(BOT_TOKEN)

# Команда /start или /hello
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот-гороскоп 🌟\nНапиши /horoscope, чтобы узнать свой прогноз.")

# Команда /horoscope — запуск сценария
@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    text = ("🪐 Какой у тебя знак зодиака?\n"
            "Выбери один из:\n*Aries*, *Taurus*, *Gemini*, *Cancer*, *Leo*, *Virgo*,\n"
            "*Libra*, *Scorpio*, *Sagittarius*, *Capricorn*, *Aquarius*, *Pisces*.")
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, day_handler)

# После выбора знака — запрашиваем дату
def day_handler(message):
    sign = message.text.strip().capitalize()
    text = ("📅 На какой день хочешь узнать гороскоп?\n"
            "Выбери: *today*, *tomorrow*, *yesterday*, или дату в формате *YYYY-MM-DD*.")
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, fetch_horoscope, sign)

# Получаем и отправляем гороскоп
def fetch_horoscope(message, sign):
    day = message.text.strip().lower()
    try:
        horoscope = get_daily_horoscope(sign, day)
        data = horoscope["data"]
        response = (
            f"*🔮 Гороскоп для {sign}*\n"
            f"{data['horoscope_data']}\n\n"
            f"*📆 День:* {data['date']}"
        )
        bot.send_message(message.chat.id, response, parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Ошибка: {e}\nПопробуй снова.", parse_mode="Markdown")

# Эхо на любое сообщение
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# Запуск бота
bot.infinity_polling()
