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

@bot.message_handler(func=lambda m: m.chat.id in user_orders and 'nickname' not in user_orders[m.chat.id])
def handle_nickname(message):
    user_orders[message.chat.id]['nickname'] = message.text
    bot.send_message(message.chat.id, "🔢 Сколько персонажей будет в позинге? (От 1 до 10):")

@bot.message_handler(func=lambda m: m.chat.id in user_orders and 'chars_count' not in user_orders[m.chat.id])
def handle_chars(message):
    text = message.text
    if text.isdigit():
        num = int(text)
        if 1 <= num <= 10:
            user_orders[message.chat.id]['chars_count'] = num
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("Робуксы", "мм2 годли", "Телеграм-звёзды")
            bot.send_message(message.chat.id, "💳 Выбери вид оплаты (ты можешь нажать другую кнопку, если передумаешь):", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, f"⚠️ Больше 10 персонажей нельзя, напишите число меньше {num}")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, введи число.")

@bot.message_handler(func=lambda m: m.chat.id in user_orders and m.text in ["Робуксы", "мм2 годли", "Телеграм-звёзды"])
def handle_payment_selection(message):
    cid = message.chat.id
    choice = message.text
    user_orders[cid]['payment_method'] = choice
    
    if choice == "Робуксы":
        msg = "💵 Вы выбрали робуксы, пожалуйста оплатите заказ по ссылке: https://www.roblox.com/games/18925562723/Позинги"
    elif choice == "мм2 годли":
        msg = "🔪 Вы выбрали годли, пожалуйста свяжитесь с владельцем (@HokhikyanHokhikyans) для оплаты."
    else:
        msg = "🌟 Вы выбрали звезды, оплатите по юзернейму @HokhikyanHokhikyans"

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Я ОПЛАТИЛ(А)", callback_data="confirm_pay"))
    bot.send_message(cid, msg, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "confirm_pay")
def final_step(call):
    cid = call.message.chat.id
    if cid in user_orders and 'payment_method' in user_orders[cid]:
        order = user_orders[cid]
        summary = (f"🔔 НОВЫЙ ЗАКАЗ!\n"
                   f"👤 Заказчик: {order['nickname']}\n"
                   f"👥 Кол-во персонажей: {order['chars_count']}\n"
                   f"💰 Оплата: {order['payment_method']}")
        
        # Отправка тебе
        bot.send_message(ADMIN_ID, summary)
        bot.send_video(ADMIN_ID, order['video_id'], caption="Видео оплаты")
        bot.send_photo(ADMIN_ID, order['photo_id'], caption="Фон")
        
        # Ответ клиенту
        bot.send_message(cid, "🚀 Все данные переданы! Ожидайте заказ. Владелец скоро свяжется с вами.", reply_markup=types.ReplyKeyboardRemove())
        del user_orders[cid]
    else:
        bot.send_message(cid, "Ошибка. Попробуйте начать заново через /start")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
