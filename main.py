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

# --- ВЕБ-СЕРВЕР ---
class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        # Получение кол-ва заказов для сайта
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

        # Логика админ-кнопки "ГОТОВО"
        elif parsed_path.path == '/order_ready':
            query = urllib.parse.parse_qs(parsed_path.query)
            target_nick = query.get('user_nick', [None])[0]
            found = False
            for uid, profile in user_profiles.items():
                if profile.get('nick') == target_nick:
                    profile['orders_count'] = profile.get('orders_count', 0) + 1
                    save_db(user_profiles)
                    bot.send_message(uid, f"✅ Ваш заказ готов! Свяжитесь с @HokhikyanHokhikyans")
                    found = True
                    break
            self.send_response(200 if found else 404)
            self.end_headers()
        else:
            super().do_GET()

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('', port), MyHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# --- ЛОГИКА БОТА (БЕЗ ПАРОЛЯ) ---
@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, "Привет! 🔥 Напиши свой ник в Roblox для регистрации:")
    bot.register_next_step_handler(msg, register_user)

def register_user(message):
    nick = message.text.strip()
    if not re.match("^[A-Za-z0-9_]+$", nick):
        msg = bot.send_message(message.chat.id, "❌ Только английские буквы и цифры! Попробуй еще раз:")
        bot.register_next_step_handler(msg, register_user)
        return

    user_profiles[str(message.chat.id)] = {
        'nick': nick,
        'orders_count': user_profiles.get(str(message.chat.id), {}).get('orders_count', 0)
    }
    save_db(user_profiles)
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🛒 СДЕЛАТЬ ЗАКАЗ", "👤 МОЙ АККАУНТ")
    bot.send_message(message.chat.id, f"✅ Аккаунт `{nick}` успешно привязан! Пароль не требуется.", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "👤 МОЙ АККАУНТ")
def my_profile(message):
    p = user_profiles.get(str(message.chat.id), {'nick': '?', 'orders_count': 0})
    bot.send_message(message.chat.id, f"👤 **ПРОФИЛЬ**\n🎮 Roblox: `{p['nick']}`\n📦 Заказов: {p['orders_count']}", parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "🛒 СДЕЛАТЬ ЗАКАЗ")
def make_order(message):
    bot.send_message(message.chat.id, "Пришлите фото или описание заказа. Админ получит уведомление!")

print("Бот и сервер запущены!")
bot.infinity_polling()
