import telebot
from telebot import types
import re
import os
import json
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

# --- НАСТРОЙКИ И БАЗА ДАННЫХ ---
TOKEN = '8595334091:AAFWypuC7IrrUG688hIlL0Nbdq4kCDLEzXU'
ADMIN_ID = 2039589760
DB_FILE = 'database.json'
bot = telebot.TeleBot(TOKEN)

# Функция для загрузки базы данных из файла
def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

# Функция для сохранения базы данных в файл
def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Инициализация данных
user_profiles = load_db()
user_orders_temp = {}

# --- БЛОК ВЕБ-СЕРВЕРА (ДЛЯ GOOGLE И RAILWAY) ---
def run_website():
    port = int(os.environ.get("PORT", 8080))
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Сайт работает на порту {port}")
    httpd.serve_forever()

threading.Thread(target=run_website, daemon=True).start()

# --- ЛОГИКА БОТА ---

@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, "Привет! 🔥 Напиши ник в Roblox (**английские буквы**):")
    bot.register_next_step_handler(msg, save_roblox_nick)

def save_roblox_nick(message):
    nick = message.text
    if not re.match("^[A-Za-z0-9_]+$", nick):
        msg = bot.send_message(message.chat.id, "❌ Только английские буквы! Попробуй еще раз:")
        bot.register_next_step_handler(msg, save_roblox_nick)
        return

    # ПРОВЕРКА: занят ли ник кем-то другим
    for uid, profile in user_profiles.items():
        if profile.get('nick') == nick and uid != str(message.chat.id):
            msg = bot.send_message(message.chat.id, f"⚠️ Ник `{nick}` уже занят! Придумай другой:")
            bot.register_next_step_handler(msg, save_roblox_nick)
            return

    msg = bot.send_message(message.chat.id, f"Ник `{nick}` свободен! Теперь придумай пароль:")
    bot.register_next_step_handler(msg, lambda m: save_password(m, nick))

def save_password(message, nick):
    password = message.text
    
    # ПРОВЕРКА: занят ли пароль кем-то другим
    for uid, profile in user_profiles.items():
        if profile.get('password') == password and uid != str(message.chat.id):
            msg = bot.send_message(message.chat.id, "⚠️ Такой пароль уже используется другим игроком. Выбери другой:")
            bot.register_next_step_handler(msg, lambda m: save_password(m, nick))
            return

    # Сохраняем аккаунт
    user_profiles[str(message.chat.id)] = {
        'nick': nick, 
        'password': password, 
        'orders_count': user_profiles.get(str(message.chat.id), {}).get('orders_count', 0)
    }
    save_db(user_profiles)
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🛒 СДЕЛАТЬ ЗАКАЗ", "👤 МОЙ АККАУНТ")
    bot.send_message(message.chat.id, f"✅ Аккаунт готов!\nНик: `{nick}`\nПароль: `{password}`", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "👤 МОЙ АККАУНТ")
def my_profile(message):
    p = user_profiles.get(str(message.chat.id), {'nick': '?', 'orders_count': 0})
    bot.send_message(message.chat.id, f"✨ **АНКЕТА**\n👤 ТГ: @{message.from_user.username}\n🎮 Roblox: `{p['nick']}`\n📦 Заказов: {p.get('orders_count', 0)}", parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "🛒 СДЕЛАТЬ ЗАКАЗ")
def ask_photo(message):
    msg = bot.send_message(message.chat.id, "📸 Пришли фото Фона:")
    bot.register_next_step_handler(msg, process_photo)

def process_photo(message):
    if message.content_type != 'photo':
        msg = bot.send_message(message.chat.id, "❌ Отправь фото!")
        bot.register_next_step_handler(msg, process_photo)
        return
    user_orders_temp[message.chat.id] = {'photo': message.photo[-1].file_id}
    markup = types.InlineKeyboardMarkup(row_width=5)
    markup.add(*[types.InlineKeyboardButton(str(i), callback_data=f"cnt_{i}") for i in range(1, 11)])
    bot.send_message(message.chat.id, "👥 Сколько персонажей (1-10)?", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith('cnt_'))
def choose_bg(call):
    user_orders_temp[call.message.chat.id]['count'] = call.data.split('_')[1]
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Прозрачный", callback_data="bg_PNG"), types.InlineKeyboardButton("Игровой", callback_data="bg_Game"))
    bot.edit_message_text("Выбери фон:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith('bg_'))
def choose_pay(call):
    user_orders_temp[call.message.chat.id]['bg'] = call.data.split('_')[1]
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💰 Робуксы", callback_data="p_Робуксы"), 
               types.InlineKeyboardButton("⚔️ Годли", callback_data="p_Годли"), 
               types.InlineKeyboardButton("⭐ Звезды", callback_data="p_Звезды"))
    bot.edit_message_text("Способ оплаты:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith('p_'))
def finish(call):
    pay = call.data.split('_')[1]
    data = user_orders_temp.get(call.message.chat.id)
    prof = user_profiles.get(str(call.message.chat.id))
    
    bot.send_message(call.message.chat.id, "готово, для подробностей напишите @HokhikyanHokhikyans")
    
    if prof:
        prof['orders_count'] = prof.get('orders_count', 0) + 1
        save_db(user_profiles)

    bot.send_photo(ADMIN_ID, data['photo'], caption=f"🚀 **ЗАКАЗ**\n👤 ТГ: @{call.from_user.username}\n🎮 Roblox: `{prof['nick'] if prof else '?'}`\n👥 Лица: {data['count']}\n🌌 Фон: {data['bg']}\n💸 Оплата: {pay}", parse_mode="Markdown")

print("Бот и Сайт запущены!")
bot.infinity_polling()
