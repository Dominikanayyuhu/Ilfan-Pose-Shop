import telebot
from telebot import types
import threading
from flask import Flask
import os

# --- 1. МИНИ-СЕРВЕР ДЛЯ ПОДДЕРЖКИ ЖИЗНИ (RENDER + CRON-JOB) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот Ильфана активен 24/7!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- 2. НАСТРОЙКА БОТА С ТВОИМИ ДАННЫМИ ---
TOKEN = '8595334091:AAFWypuC7IrrUG688hIlL0Nbdq4kCDLEzXU'
ADMIN_ID = 2039589760
bot = telebot.TeleBot(TOKEN)

# Временное хранилище для данных заказа
user_data = {}

# --- 3. ЛОГИКА БОТА ---

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🛒 КАТАЛОГ ПОЗ"), types.KeyboardButton("👤 МОЙ АККАУНТ"))
    
    bot.send_message(message.chat.id, 
                     f"Привет, {message.from_user.first_name}! 🔥\nЯ помогу тебе заказать крутую позу. Выбери раздел:", 
                     reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🛒 КАТАЛОГ ПОЗ")
def catalog(message):
    markup = types.InlineKeyboardMarkup(row_width=3)
    btns = [types.InlineKeyboardButton(f"Поза #{i}", callback_data=f"pose_{i}") for i in range(1, 12)]
    markup.add(*btns)
    bot.send_message(message.chat.id, "Выбери номер позы для заказа:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('pose_'))
def choose_skins(call):
    pose_id = call.data.split('_')[1]
    user_data[call.message.chat.id] = {'pose': pose_id}
    
    markup = types.InlineKeyboardMarkup()
    for i in range(1, 5):
        markup.add(types.InlineKeyboardButton(f"{i} Персонаж(а)", callback_data=f"sk_{i}"))
    
    bot.edit_message_text(f"Выбрана Поза #{pose_id}. Сколько персонажей добавить?", 
                          chat_id=call.message.chat.id, 
                          message_id=call.message.message_id, 
                          reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('sk_'))
def choose_bg(call):
    skins = call.data.split('_')[1]
    user_data[call.message.chat.id]['skins'] = skins
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Прозрачный (PNG)", callback_data="bg_png"),
               types.InlineKeyboardButton("Игровой фон (Карта)", callback_data="bg_game"))
    
    bot.edit_message_text(f"Персонажей: {skins}. Выбери тип фона:", 
                          chat_id=call.message.chat.id, 
                          message_id=call.message.message_id, 
                          reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('bg_'))
def choose_pay(call):
    bg = "Прозрачный" if "png" in call.data else "Игровой"
    user_data[call.message.chat.id]['bg'] = bg
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💳 КАРТА", callback_data="p_card"),
               types.InlineKeyboardButton("💎 КРИПТА / LIKECOIN", callback_data="p_crypto"))
    
    bot.edit_message_text(f"Выбран фон: {bg}.\nВыбери удобный способ оплаты:", 
                          chat_id=call.message.chat.id, 
                          message_id=call.message.message_id, 
                          reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('p_'))
def final(call):
    pay_method = "Карта" if "card" in call.data else "Крипта"
    data = user_data.get(call.message.chat.id)
    
    # 1. Сообщение КЛИЕНТУ (как ты просил)
    bot.send_message(call.message.chat.id, "готово, для подробностей напишите владельцу магазина @HokhikyanHokhikyans, чтобы вы могли забрать заказ")
    
    # 2. Уведомление ТЕБЕ (Админу) со всеми данными
    admin_text = (f"🚀 НОВЫЙ ЗАКАЗ!\n\n"
                  f"👤 Ник клиента: @{call.from_user.username}\n"
                  f"🆔 ID: {call.from_user.id}\n"
                  f"🖼 Поза: #{data['pose']}\n"
                  f"👥 Кол-во персонажей: {data['skins']}\n"
                  f"🌌 Фон: {data['bg']}\n"
                  f"💰 Оплата: {pay_method}")
    bot.send_message(ADMIN_ID, admin_text)

# --- 4. ЗАПУСК ---
if __name__ == '__main__':
    threading.Thread(target=run_web_server, daemon=True).start()
    print("Бот успешно запущен!")
    bot.infinity_polling()

    
