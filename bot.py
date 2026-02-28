import telebot
import os

TOKEN = os.environ.get("TOKEN")

if not TOKEN:
    print("TOKEN topilmadi")
    exit()

bot = telebot.TeleBot(TOKEN)

anime_db = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot ishlayapti 😎")

@bot.message_handler(commands=['add'])
def add_anime(message):
    if message.from_user.id != 7349426325:
        return

    try:
        _, anime_id, title, episodes = message.text.split()
        anime_db[anime_id] = {
            "title": title,
            "episodes": int(episodes)
        }
        bot.reply_to(message, "Anime qo‘shildi ✅")
    except:
        bot.reply_to(message, "Format: /add id nomi qism_soni")

@bot.message_handler(func=lambda m: True)
def send_anime(message):
    if message.text in anime_db:
        anime = anime_db[message.text]
        bot.send_message(
            message.chat.id,
            f"{anime['title']} ({anime['episodes']} qism)"
        )
    else:
        bot.reply_to(message, "Topilmadi ❌")

print("Bot ishga tushdi...")
bot.infinity_polling()
