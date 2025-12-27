import telebot
from telebot import types
from flask import Flask
from threading import Thread
import os

app = Flask('')
@app.route('/')
def home(): return "Бот работает!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    Thread(target=run).start()

API_TOKEN = '8595334091:AAFWypuC7IrrUG688hIlL0Nbdq4kCDLEzXU'
ADMIN_ID = 2039589760 
bot = telebot.TeleBot(API_TOKEN)

user_orders = {}

@bot.message_handler(commands=['start'])
def start(message):
    shop_link = "https://dominikanayyuhu.github.io/Ilfan-Pose-Shop/" 
    bot.send_message(message.chat.id, f"👋 Привет! Магазин тут: {shop_link}\n🎬 Пришли видео оплаты для заказа.")

@bot.message_handler(content_types=['video', 'video_note'])
def handle_payment_video(message):
    user_orders[message.chat.id] = {'video_id': message.video.file_id if message.video else message.video_note.file_id}
    bot.send_message(message.chat.id, "🖼 Теперь пришли ФОН (скриншот или картинку):")

@bot.message_handler(content_types=['photo'])
def handle_background(message):
    if message.chat.id in user_orders:
        user_orders[message.chat.id]['photo_id'] = message.photo[-1].file_id
        bot.send_message(message.chat.id, "👤 Напиши свой ник в Roblox:")
    else:
        bot.send_message(message.chat.id, "Сначала пришли видео оплаты!")

@bot.message_handler(func=lambda message: message.chat.id in user_orders and 'nickname' not in user_orders[message.chat.id])
def handle_nickname(message):
    user_orders[message.chat.id]['nickname'] = message.text
    bot.send_message(message.chat.id, "🔢 Сколько персонажей будет в позинге? (От 1 до 10):")

@bot.message_handler(func=lambda message: message.chat.id in user_orders and 'chars_count' not in user_orders[message.chat.id])
def handle_chars(message):
    text = message.text
    if text.isdigit():
        num = int(text)
        if 1 <= num <= 10:
            user_orders[message.chat.id]['chars_count'] = num
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add("Робуксы", "мм2 годли", "Телеграм-звёзды")
            bot.send_message(message.chat.id, "💳 Выбери вид оплаты:", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, f"⚠️ Больше 10 персонажей нельзя, напишите число меньше {num + 1}")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, введи число.")

@bot.message_handler(func=lambda message: message.chat.id in user_orders and 'payment_method' not in user_orders[message.chat.id])
def handle_payment_method(message):
    choice = message.text
    chat_id = message.chat.id
    order = user_orders[chat_id]
    
    if choice == "Робуксы":
        order['payment_method'] = choice
        bot.send_message(chat_id, "💵 Вы выбрали робуксы, поэтому пожалуйста оплатите заказ по ссылке: https://www.roblox.com/games/12345 (Пример ссылки)\n✅ После этого заказ будет передан админу.")
        send_order_to_admin(chat_id)
    elif choice == "мм2 годли":
        order['payment_method'] = choice
        bot.send_message(chat_id, "🔪 Вы выбрали годли, пожалуйста свяжитесь с владельцем (@HokhikyanHokhikyans), чтобы оплатить заказ.")
        send_order_to_admin(chat_id)
    elif choice == "Телеграм-звёзды":
        order['payment_method'] = choice
        bot.send_message(chat_id, "🌟 Вы выбрали телеграм звёзды, пожалуйста оплатите заказ по этому юзернейму (@HokhikyanHokhikyans). Жду подтверждения.")
        send_order_to_admin(chat_id)
    else:
        bot.send_message(chat_id, "❌ Недопустимый ответ, пожалуйста выберите из 3 вариантов в меню.")

def send_order_to_admin(chat_id):
    order = user_orders[chat_id]
    summary = (f"📝 АНКЕТА ЗАКАЗА\n"
               f"👤 Заказчик: {order['nickname']}\n"
               f"👥 Кол-во персонажей: {order['chars_count']}\n"
               f"💰 Оплата: {order['payment_method']}")
    
    bot.send_message(ADMIN_ID, summary)
    bot.send_video(ADMIN_ID, order['video_id'], caption="Видео-доказательство")
    bot.send_photo(ADMIN_ID, order['photo_id'], caption="Выбранный фон")
    
    bot.send_message(chat_id, "🚀 Все данные переданы! Ожидайте готовности.")
    del user_orders[chat_id]

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
