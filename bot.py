import telebot
import os
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 7349426325 # <-- O'Z IDINGNI YOZ

DB_FILE = "anime.json"

# Agar fayl yo‘q bo‘lsa yaratadi
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({}, f)

def load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🔎 Qidirish"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "🎌 Anime Olamiga xush kelibsiz!",
                     reply_markup=main_menu())

@bot.message_handler(commands=['add'])
def add_anime(message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        _, name, link = message.text.split(" ", 2)
        data = load_db()
        data[name.lower()] = link
        save_db(data)
        bot.send_message(message.chat.id, "✅ Saqlandi yoki yangilandi!")
    except:
        bot.send_message(message.chat.id, "❌ Format: /add nom link")

@bot.message_handler(func=lambda message: True)
def search(message):
    data = load_db()
    text = message.text.lower()

    if text in data:
        bot.send_message(message.chat.id, data[text])
    else:
        bot.send_message(message.chat.id, "❌ Anime topilmadi")

bot.polling()
