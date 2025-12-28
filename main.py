import telebot
from telebot import types
import threading
from flask import Flask
import os
import re  # Импортируем библиотеку для проверки текста

# --- 1. ВЕБ-СЕРВЕР ДЛЯ ПОДДЕРЖКИ ЖИЗНИ ---
app = Flask(__name__)
@app.route('/')
def home(): return "Бот Ильфана активен 24/7!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- 2. НАСТРОЙКА БОТА ---
TOKEN = '8595334091:AAFWypuC7IrrUG688hIlL0Nbdq4kCDLEzXU'
ADMIN_ID = 2039589760
bot = telebot.TeleBot(TOKEN)

user_profiles = {} 
user_orders_temp = {} 

# --- 3. ЛОГИКА РЕГИСТРАЦИИ ---

@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, "Привет! 🔥 Давай настроим твой профиль.\n\n**Напиши свой ник в Roblox (только английские буквы):**", parse_mode="Markdown")
    bot.register_next_step_handler(msg, save_roblox_nick)

def save_roblox_nick(message):
    nick = message.text
    # Проверка: разрешаем только английские буквы, цифры и символ подчеркивания
    if not re.match("^[A-Za-z0-9_]+$", nick):
        msg = bot.send_message(message.chat.id, "❌ Ошибка! Ник должен содержать **только английские буквы** и цифры. Попробуй еще раз:")
        bot.register_next_step_handler(msg, save_roblox_nick)
        return

    user_profiles[message.chat.id] = {'nick': nick, 'orders_count': 0}
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🛒 СДЕЛАТЬ ЗАКАЗ"), types.KeyboardButton("👤 МОЙ АККАУНТ"))
    
    bot.send_message(message.chat.id, f"✅ Профиль настроен!\n🎮 Твой ник: {nick}", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "👤 МОЙ АККАУНТ")
def my_profile(message):
    profile = user_profiles.get(message.chat.id)
    if not profile:
        bot.send_message(message.chat.id, "Сначала введи /start!")
        return

    text = (f"✨ **ТВОЯ АНКЕТА** ✨\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👤 **Юзернейм ТГ:** @{message.from_user.username}\n"
            f"🎮 **Ник Roblox:** `{profile['nick']}`\n"
            f"📦 **Заказов сделано:** {profile['orders_count']}\n"
            f"━━━━━━━━━━━━━━━━━━")
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# --- 4. ПРОЦЕСС ЗАКАЗА ---

@bot.message_handler(func=lambda message: message.text == "🛒 СДЕЛАТЬ ЗАКАЗ")
def ask_for_photo(message):
    msg = bot.send_message(message.chat.id, "📸 Пришли **фото или скриншот** позинга:")
    bot.register_next_step_handler(msg, process_photo)

def process_photo(message):
    if message.content_type != 'photo':
        msg = bot.send_message(message.chat.id, "❌ Отправь именно фото!")
        bot.register_next_step_handler(msg, process_photo)
        return
    
    user_orders_temp[message.chat.id] = {'photo': message.photo[-1].file_id}
    
    markup = types.InlineKeyboardMarkup(row_width=5)
    btns = [types.InlineKeyboardButton(str(i), callback_data=f"cnt_{i}") for i in range(1, 11)]
    markup.add(*btns)
    bot.send_message(message.chat.id, "👥 Количество персонажей (1-10):", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('cnt_'))
def choose_bg(call):
    count = call.data.split('_')[1]
    user_orders_temp[call.message.chat.id]['count'] = count
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Прозрачный (PNG)", callback_data="bg_PNG"),
               types.InlineKeyboardButton("Игровой фон", callback_data="bg_Игровой"))
    bot.edit_message_text(f"Выбрано персонажей: {count}. Выбери фон:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('bg_'))
def choose_payment(call):
    bg_type = call.data.split('_')[1]
    user_orders_temp[call.message.chat.id]['bg'] = bg_type
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💰 Робуксы", callback_data="p_Робуксы"),
               types.InlineKeyboardButton("⚔️ Годли", callback_data="p_Годли"),
               types.InlineKeyboardButton("⭐ Звезды", callback_data="p_Звезды"))
    bot.edit_message_text(f"Фон: {bg_type}. Выбери способ оплаты:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('p_'))
def finish_order(call):
    pay_method = call.data.split('_')[1]
    data = user_orders_temp.get(call.message.chat.id)
    profile = user_profiles.get(call.message.chat.id)
    
    bot.send_message(call.message.chat.id, "готово, для подробностей напишите владельцу магазина @HokhikyanHokhikyans, чтобы вы могли забрать заказ")
    
    if profile: profile['orders_count'] += 1
    
    bot.send_photo(ADMIN_ID, data['photo'], caption=(
        f"🚀 **НОВЫЙ ЗАКАЗ!**\n\n"
        f"👤 **Ник ТГ:** @{call.from_user.username}\n"
        f"🎮 **Ник Roblox:** `{profile['nick'] if profile else 'Неизвестно'}`\n"
        f"👥 **Персонажей:** {data['count']}\n"
        f"🌌 **Фон:** {data['bg']}\n"
        f"💸 **Оплата:** {pay_method}"
    ), parse_mode="Markdown")

if __name__ == '__main__':
    threading.Thread(target=run_web_server, daemon=True).start()
    bot.infinity_polling()
    
    
    
