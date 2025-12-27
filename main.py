import telebot
from flask import Flask
from threading import Thread
import os

# --- СЕРВЕР ДЛЯ RENDER ---
app = Flask('')
@app.route('/')
def home(): return "Бот работает!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    Thread(target=run).start()

# --- НАСТРОЙКИ БОТА ---
API_TOKEN = '8595334091:AAFWypuC7IrrUG688hIlL0Nbdq4kCDLEzXU'
ADMIN_ID = 2039589760  # Твой ID
bot = telebot.TeleBot(API_TOKEN)

# Словарь для хранения данных о заказе
user_orders = {}

@bot.message_handler(commands=['start'])
def start(message):
    shop_link = "https://dominikanayyuhu.github.io/Ilfan-Pose-Shop/" 
    bot.send_message(message.chat.id, f"👋 Привет! Магазин тут: {shop_link}\n🎬 Пришли видео оплаты для заказа.")

@bot.message_handler(content_types=['video', 'video_note'])
def handle_payment(message):
    user_orders[message.chat.id] = {'video_id': message.video.file_id if message.video else message.video_note.file_id}
    bot.send_message(message.chat.id, "✅ Видео получено! Теперь напиши свой ник в Roblox:")

@bot.message_handler(content_types=['text'])
def handle_nickname(message):
    chat_id = message.chat.id
    if chat_id in user_orders:
        nickname = message.text
        video_id = user_orders[chat_id]['video_id']
        
        # Отвечаем пользователю
        bot.send_message(chat_id, f"✅ Заказ принят, {nickname}! Скоро я проверю оплату и выдам позу.")
        
        # Отправляем уведомление ТЕБЕ (админу)
        bot.send_message(ADMIN_ID, f"🔔 НОВЫЙ ЗАКАЗ!\n👤 Ник: {nickname}\n🆔 ID: {chat_id}")
        bot.send_video(ADMIN_ID, video_id)
        
        # Очищаем данные заказа
        del user_orders[chat_id]
    else:
        bot.send_message(chat_id, "Сначала пришли видео оплаты!")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
