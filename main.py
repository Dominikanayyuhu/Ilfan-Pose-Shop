import telebot
from telebot import types
import threading
from flask import Flask
import os

# --- 1. ВЕБ-СЕРВЕР ДЛЯ ПОДДЕРЖКИ ЖИЗНИ ---
app = Flask(__name__)
@app.route('/')
def home(): return "Бот Ильфана активен!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- 2. НАСТРОЙКА БОТА ---
TOKEN = '8595334091:AAFWypuC7IrrUG688hIlL0Nbdq4kCDLEzXU'
ADMIN_ID = 2039589760
bot = telebot.TeleBot(TOKEN)

# Хранилища данных
user_profiles = {} 
user_orders_data = {} 

@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, "Привет! 🔥 Давай настроим твой профиль.\n\n**Напиши свой ник в Roblox:**", parse_mode="Markdown")
    bot.register_next_step_handler(msg, save_roblox_nick)

def save_roblox_nick(message):
    user_profiles[message.chat.id] = {'nick': message.text, 'orders_count': 0}
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🛒 СДЕЛАТЬ ЗАКАЗ"), types.KeyboardButton("👤 МОЙ АККАУНТ"))
    
    bot.send_message(message.chat.id, f"✅ Профиль настроен!\n🎮 Ник: {message.text}\n\nТеперь ты можешь заказать позинг через меню.", reply_markup=markup)

# --- КНОПКА: МОЙ АККАУНТ ---
@bot.message_handler(func=lambda message: message.text == "👤 МОЙ АККАУНТ")
def my_profile(message):
    profile = user_profiles.get(message.chat.id)
    if not profile:
        bot.send_message(message.chat.id, "Сначала нажми /start, чтобы создать анкету!")
        return

    text = (f"✨ **ТВОЯ КРЕАТИВНАЯ АНКЕТА** ✨\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👤 **Юзернейм:** @{message.from_user.username}\n"
            f"🎮 **Ник Roblox:** `{profile['nick']}`\n"
            f"📦 **Заказов сделано:** {profile['orders_count']}\n"
            f"━━━━━━━━━━━━━━━━━━")
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# --- КНОПКА: ЗАКАЗ ---
@bot.message_handler(func=lambda message: message.text == "🛒 СДЕЛАТЬ ЗАКАЗ")
def ask_for_photo(message):
    msg = bot.send_message(message.chat.id, "📸 Пришли **фото или скриншот** (пример позинга), который ты хочешь:")
    bot.register_next_step_handler(msg, process_photo)

def process_photo(message):
    if message.content_type != 'photo':
        msg = bot.send_message(message.chat.id, "Ошибка! Пожалуйста, отправь именно **фото**.")
        bot.register_next_step_handler(msg, process_photo)
        return
    
    user_orders_data[message.chat.id] = {'photo': message.photo[-1].file_id}
    
    # Выбор количества персонажей (от 1 до 10)
    markup = types.InlineKeyboardMarkup(row_width=5)
    btns = [types.InlineKeyboardButton(str(i), callback_data=f"pcount_{i}") for i in range(1, 11)]
    markup.add(*btns)
    
    bot.send_message(message.chat.id, "👥 Сколько персонажей будет в позинге? (Максимум 10):", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('pcount_'))
def choose_bg(call):
    count = call.data.split('_')[1]
    user_orders_data[call.message.chat.id]['count'] = count
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Прозрачный (PNG)", callback_data="setbg_PNG"),
               types.InlineKeyboardButton("Игровой фон", callback_data="setbg_Игровой"))
    
    bot.edit_message_text(f"Персонажей: {count}. Теперь выбери фон:", 
                          chat_id=call.message.chat.id, 
                          message_id=call.message.message_id, 
                          reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('setbg_'))
def choose_payment(call):
    bg = call.data.split('_')[1]
    user_orders_data[call.message.chat.id]['bg'] = bg
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💰 Робуксы", callback_data="pay_Робуксы"),
               types.InlineKeyboardButton("⚔️ Годли", callback_data="pay_Годли"),
               types.InlineKeyboardButton("⭐ Звезды", callback_data="pay_Звезды"))
    
    bot.edit_message_text(f"Выбран фон: {bg}. Выбери способ оплаты:", 
                          chat_id=call.message.chat.id, 
                          message_id=call.message.message_id, 
                          reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('pay_'))
def finish_order(call):
    method = call.data.split('_')[1]
    data = user_orders_data.get(call.message.chat.id)
    profile = user_profiles.get(call.message.chat.id)
    
    # 1. Ответ клиенту
    bot.send_message(call.message.chat.id, "готово, для подробностей напишите владельцу магазина @HokhikyanHokhikyans, чтобы вы могли забрать заказ")
    
    # 2. Обновляем счетчик заказов
    if profile: profile['orders_count'] += 1
    
    # 3. Полный отчет ТЕБЕ (Админу)
    bot.send_photo(ADMIN_ID, data['photo'], caption=(
        f"🚀 **НОВЫЙ ЗАКАЗ!**\n\n"
        f"👤 **Ник ТГ:** @{call.from_user.username}\n"
        f"🎮 **Ник Roblox:** `{profile['nick']}`\n"
        f"👥 **Персонажей:** {data['count']}\n"
        f"🌌 **Фон:** {data['bg']}\n"
        f"💸 **Оплата:** {method}"
    ), parse_mode="Markdown")

# --- 4. ЗАПУСК ---
if __name__ == '__main__':
    threading.Thread(target=run_web_server, daemon=True).start()
    bot.infinity_polling()
    
    
