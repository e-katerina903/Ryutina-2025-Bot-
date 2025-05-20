import os
import telebot
import csv

BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не установлен")

bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! 🧵 Я принимаю заявки на пошив постельного белья.\nДавайте начнём! Как вас зовут?")
    user_data[message.chat.id] = {}
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_data[message.chat.id]['name'] = message.text
    bot.send_message(message.chat.id, "Укажите, пожалуйста, ваш номер телефона 📱:")
    bot.register_next_step_handler(message, get_phone)

def get_phone(message):
    user_data[message.chat.id]['phone'] = message.text
    bot.send_message(message.chat.id, "Какой размер комплекта вы хотите? (например: односпальный, двуспальный, евро)")
    bot.register_next_step_handler(message, get_size)

def get_size(message):
    user_data[message.chat.id]['size'] = message.text
    bot.send_message(message.chat.id, "Есть ли пожелания к ткани, цвету или другие комментарии?")
    bot.register_next_step_handler(message, get_comment)

def get_comment(message):
    user_data[message.chat.id]['comment'] = message.text
    save_to_csv(user_data[message.chat.id])
    bot.send_message(message.chat.id, "Спасибо! Ваша заявка принята. Мы с вами скоро свяжемся ✂️🧵")
    user_data.pop(message.chat.id, None)

def save_to_csv(data):
    file_exists = os.path.isfile("orders.csv")
    with open("orders.csv", "a", newline="", encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["name", "phone", "size", "comment"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.send_message(message.chat.id, "Чтобы оставить заявку, напишите /start")

bot.infinity_polling()

