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
ADMIN_ID = '2039589760' 
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    shop_link = "https://dominikanayyuhu.github.io/Ilfan-Pose-Shop/" 
    bot.send_message(message.chat.id, f"👋 Привет! Магазин тут: {shop_link}\n🎬 Пришли видео оплаты для заказа.")

@bot.message_handler(content_types=['video'])
def handle_payment(message):
    bot.send_message(message.chat.id, "✅ Получено! Напиши свой ник в Roblox:")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
