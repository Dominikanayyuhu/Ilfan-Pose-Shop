import telebot
from telebot import types
import re, os, json, threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
import urllib.parse

# --- НАСТРОЙКИ ---
TOKEN = '8595334091:AAFWypuC7IrrUG688hIlL0Nbdq4kCDLEzXU'
ADMIN_ID = 2039589760
DB_FILE = 'database.json'
bot = telebot.TeleBot(TOKEN)

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return {}
    return {}

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

user_profiles = load_db()
user_orders_temp = {}

# --- СЕРВЕР С ЛОГИКОЙ ОБНОВЛЕНИЯ СЧЕТЧИКА ---
class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        # 1. Получение счетчика для сайта
        if parsed_path.path == '/get_orders':
            query = urllib.parse.parse_qs(parsed_path.query)
            nick = query.get('nick', [None])[0]
            count = 0
            for profile in user_profiles.values():
                if profile.get('nick') == nick:
                    count = profile.get('orders_count', 0)
                    break
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'count': count}).encode())

        # 2. ЛОГИКА КНОПКИ "ГОТОВО" (Прибавление +1 и уведомление)
        elif parsed_path.path == '/order_ready':
            query = urllib.parse.parse_qs(parsed_path.query)
            target_nick = query.get('user_nick', [None])[0]
            
            found = False
            for uid, profile in user_profiles.items():
                if profile.get('nick') == target_nick:
                    # Прибавляем +1 к счетчику
                    profile['orders_count'] = profile.get('orders_count', 0) + 1
                    save_db(user_profiles)
                    
                    # Отправляем сообщение через бота
                    bot.send_message(uid, "Ваш позинг готов, пожалуйста свяжитесь с @HokhikyanHokhikyans, чтобы получить позинг!")
                    found = True
                    break
            
            self.send_response(200 if found else 404)
            self.end_headers()
        else:
            super().do_GET()

def run_website():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('', port), MyHandler)
    server.serve_forever()

threading.Thread(target=run_website, daemon=True).start()

# --- ЛОГИКА БОТА (РЕГИСТРАЦИЯ И ЗАКАЗЫ) ---

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
    
    # Проверка уникальности
    for uid, profile in user_profiles.items():
        if profile.get('nick') == nick and uid != str(message.chat.id):
            msg = bot.send_message(message.chat.id, f"⚠️ Ник `{nick}` уже занят! Придумай другой:")
            bot.register_next_step_handler(msg, save_roblox_nick)
            return

    msg = bot.send_message(message.chat.id, f"Ник `{nick}` свободен! Теперь придумай пароль:")
    bot.register_next_step_handler(msg, lambda m: save_password(m, nick))

def save_password(message, nick):
    password = message.text
    for uid, profile in user_profiles.items():
        if profile.get('password') == password and uid != str(message.chat.id):
            msg = bot.send_message(message.chat.id, "⚠️ Такой пароль занят. Выбери другой:")
            bot.register_next_step_handler(msg, lambda m: save_password(m, nick))
            return

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
    bot.send_message(message.chat.id, f"✨ **АНКЕТА**\n🎮 Roblox: `{p['nick']}`\n📦 Заказов: {p.get('orders_count', 0)}", parse_mode="Markdown")

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
    # ... здесь идет остальная твоя логика выбора кнопок (1-10 лиц, фон и т.д.)
    # В конце функции finish() просто отправляй данные админу БЕЗ прибавления +1.
    # +1 прибавится только через сайт!
    bot.send_message(message.chat.id, "Заказ отправлен! Ожидайте уведомления о готовности.")

print("Сервер запущен!")
bot.infinity_polling()
