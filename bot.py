import telebot
import json
import os

TOKEN = "BU_YERGA_TOKENINGNI_QO'Y"
ADMIN_ID = 7349426325
CHANNEL_LINK = "https://t.me/animuz_olami"

bot = telebot.TeleBot(TOKEN)

DB_FILE = "anime_db.json"
USER_FILE = "users.json"

# ================= LOAD / SAVE =================

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_users():
    if not os.path.exists(USER_FILE):
        return []
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(USER_FILE, "w") as f:
        json.dump(data, f)

anime_db = load_db()
users = load_users()

# ================= START =================

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id not in users:
        users.append(message.from_user.id)
        save_users(users)

    bot.send_message(
        message.chat.id,
        "🎬 Anime botga xush kelibsiz!\n\n"
        "Anime raqamini yuboring (masalan: 15)"
    )

# ================= STAT =================

@bot.message_handler(commands=['stat'])
def stat(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id,
                         f"📊 Foydalanuvchilar: {len(users)} ta")
    else:
        bot.send_message(message.chat.id, "❌ Siz admin emassiz")

# ================= ADD ANIME =================
# Format:
/add 15 Naruto 12 https://image_link.jpg

@bot.message_handler(commands=['add'])
def add_anime(message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        parts = message.text.split()
        anime_id = parts[1]
        name = parts[2]
        ep_count = int(parts[3])
        image = parts[4]

        anime_db[anime_id] = {
            "name": name,
            "episodes": ep_count,
            "image": image
        }

        save_db(anime_db)
        bot.send_message(message.chat.id, "✅ Anime saqlandi!")

    except:
        bot.send_message(message.chat.id,
                         "❌ Format:\n/add 15 Naruto 12 https://img.jpg")

# ================= NUMBER SEND =================

@bot.message_handler(func=lambda message: message.text.isdigit())
def send_all_episodes(message):
    anime_id = message.text

    if anime_id not in anime_db:
        bot.send_message(message.chat.id, "❌ Anime topilmadi")
        return

    anime = anime_db[anime_id]

    # Rasm bilan nom chiqadi
    bot.send_photo(
        message.chat.id,
        anime["image"],
        caption=f"📺 {anime['name']}\n\n🎬 Barcha qismlar 👇"
    )

    # Barcha qismlar ketma-ket
    for ep in range(1, anime["episodes"] + 1):
        link = f"{CHANNEL_LINK}/{ep}"
        bot.send_message(
            message.chat.id,
            f"{anime['name']} - Qism {ep}\n{link}"
        )

print("Bot ishlayapti...")
bot.infinity_polling()
