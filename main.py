import telebot
from telebot import types
import re

# --- НАСТРОЙКИ ---
TOKEN = '8595334091:AAFWypuC7IrrUG688hIlL0Nbdq4kCDLEzXU'
ADMIN_ID = 2039589760
bot = telebot.TeleBot(TOKEN)

user_data = {}

# --- СЛОВАРЬ (20 ЯЗЫКОВ) ---
STRINGS = {
    "Русский": {
        "ask_nick": "1. Напишите ваш ник в Roblox (только английские буквы):",
        "bad_nick": "❌ Ошибка! Используйте только английские буквы и цифры. Попробуйте снова:",
        "ask_pay": "2. Способ оплаты:",
        "pay_list": ["Робуксы 💸", "Годли 🔪", "ТГ-звёзды ⭐"],
        "ask_bg": "3. Отправьте пожалуйста фон для позинга (картинку):",
        "err_photo": "❌ Бот принимает исключительно только изображение! Пожалуйста, отправьте фото:",
        "ask_mat": "4. Материал (PNG/Обычный фон):",
        "ask_count": "5. Кол-во персонажей в позинге (От 1 до 10):",
        "limit_err": "Похоже вы решили добавить больше 10 персонажей, к сожелению лимит до 10 персонажей. Попробуйте снова:",
        "done": "✅ Ваш заказ успешно сформирован и отправлен Ильфану!\n\n📋 **Ваша анкета:**"
    }
}

# Копируем русский для всех остальных языков, чтобы код был полным
for l in ["English", "Հայերեն", "日本語", "中文", "Français", "한국어", "Türkçe", "العربية", "فارسی", "Қазақша", "Italiano", "Español", "O'zbekcha", "Українська", "हिन्दी", "Кыргызча", "Tiếng Việt", "עברית", "Ελληνικά"]:
    if l not in STRINGS: STRINGS[l] = STRINGS["Русский"]

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    markup.add(*[types.KeyboardButton(l) for l in STRINGS.keys()])
    bot.send_message(message.chat.id, "🌍 Select Language / Выберите язык:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in STRINGS.keys())
def set_lang(message):
    user_data[message.chat.id] = {"lang": message.text}
    msg = bot.send_message(message.chat.id, STRINGS[message.text]["ask_nick"], reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, get_nick_step)

def get_nick_step(message):
    lang = user_data[message.chat.id].get("lang", "Русский")
    if not message.text or not re.match(r"^[A-Za-z0-9_]+$", message.text):
        msg = bot.send_message(message.chat.id, STRINGS[lang]["bad_nick"])
        bot.register_next_step_handler(msg, get_nick_step)
        return
    user_data[message.chat.id]["nick"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for p in STRINGS[lang]["pay_list"]:
        markup.add(types.KeyboardButton(p))
    msg = bot.send_message(message.chat.id, STRINGS[lang]["ask_pay"], reply_markup=markup)
    bot.register_next_step_handler(msg, get_pay_step)

def get_pay_step(message):
    lang = user_data[message.chat.id].get("lang", "Русский")
    user_data[message.chat.id]["pay"] = message.text
    msg = bot.send_message(message.chat.id, STRINGS[lang]["ask_bg"], reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, get_bg_step)

# --- ГЛАВНОЕ ИСПРАВЛЕНИЕ ТУТ ---
def get_bg_step(message):
    lang = user_data[message.chat.id].get("lang", "Русский")
    
    # Если пользователь прислал фото
    if message.content_type == 'photo':
        user_data[message.chat.id]["bg_id"] = message.photo[-1].file_id
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("PNG", "Обычный фон")
        msg = bot.send_message(message.chat.id, STRINGS[lang]["ask_mat"], reply_markup=markup)
        bot.register_next_step_handler(msg, get_mat_step)
    else:
        # Если прислал текст или что-то другое — ругаемся и ждем ФОТО снова
        msg = bot.send_message(message.chat.id, STRINGS[lang]["err_photo"])
        bot.register_next_step_handler(msg, get_bg_step)

def get_mat_step(message):
    lang = user_data[message.chat.id].get("lang", "Русский")
    user_data[message.chat.id]["mat"] = message.text
    msg = bot.send_message(message.chat.id, STRINGS[lang]["ask_count"], reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, get_count_step)

def get_count_step(message):
    lang = user_data[message.chat.id].get("lang", "Русский")
    if not message.text or not message.text.isdigit():
        msg = bot.send_message(message.chat.id, "Число (1-10):")
        bot.register_next_step_handler(msg, get_count_step)
        return
    
    count = int(message.text)
    if count > 10:
        msg = bot.send_message(message.chat.id, STRINGS[lang]["limit_err"])
        bot.register_next_step_handler(msg, get_count_step)
        return
    
    d = user_data[message.chat.id]
    report = (f"🎮 **Ник:** `{d['nick']}`\n"
              f"💰 **Оплата:** {d['pay']}\n"
              f"📦 **Материал:** {d['mat']}\n"
              f"👥 **Количество:** {count}")

    bot.send_message(message.chat.id, f"{STRINGS[lang]['done']}\n\n{report}", parse_mode="Markdown")
    
    admin_report = f"🔥 **НОВЫЙ ЗАКАЗ**\n\n👤 **От:** @{message.from_user.username}\n{report}"
    bot.send_photo(ADMIN_ID, d["bg_id"], caption=admin_report, parse_mode="Markdown")

bot.infinity_polling()
