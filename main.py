import telebot
from telebot import types
import threading
from flask import Flask
import os

# --- 1. МИНИ-СЕРВЕР ДЛЯ ПОДДЕРЖКИ ЖИЗНИ (ЧТОБЫ RENDER НЕ СПАЛ) ---
app = Flask(__name__)

@app.route('/')
def home():
    # Этот текст увидит Cron-job, когда будет заходить по ссылке
    return "Бот Ильфана работает 24/7!"

def run_web_server():
    # Порт 10000 или тот, который даст Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- 2. ЛОГИКА ТВОЕГО БОТА ---
TOKEN = 'ТВОЙ_ТОКЕН_ОТ_BOTFATHER'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🛒 КАТАЛОГ ПОЗ"), types.KeyboardButton("👤 МОЙ АККАУНТ"))
    
    bot.send_message(
        message.chat.id, 
        f"Добро пожаловать в Ilfan's Poses Premium, {message.from_user.first_name}! 🔥\nВыбери нужный раздел ниже:", 
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "🛒 КАТАЛОГ ПОЗ")
def catalog(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    # Создаем кнопки для всех 11 поз
    buttons = [types.InlineKeyboardButton(f"Поза #{i}", callback_data=f"buy_{i}") for i in range(1, 12)]
    markup.add(*buttons)
    
    bot.send_message(message.chat.id, "Выберите позу для покупки:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def choose_payment(call):
    pose_id = call.data.split('_')[1]
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("💳 КАРТА (РФ/СНГ)", callback_data=f"pay_card_{pose_id}")
    btn2 = types.InlineKeyboardButton("💎 КРИПТА / LIKECOIN", callback_data=f"pay_crypto_{pose_id}")
    markup.add(btn1, btn2)
    
    bot.edit_message_text(
        f"Вы выбрали Позу #{pose_id}. Выберите способ оплаты:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('pay_'))
def final(call):
    method = "Карта" if "card" in call.data else "Крипта"
    bot.send_message(call.message.chat.id, f"✅ Заявка создана!\nСпособ: {method}\n\nНапишите администратору @ТВОЙ_НИК для оплаты и получения файла.")

# --- 3. ЗАПУСК ДВУХ ПРОЦЕССОВ ОДНОВРЕМЕННО ---
if __name__ == '__main__':
    # Сначала запускаем сервер-будильник в фоновом потоке
    server_thread = threading.Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()
    
    print("Веб-сервер запущен. Бот начинает работу...")
    
    # Теперь запускаем самого бота
    bot.infinity_polling()
    
