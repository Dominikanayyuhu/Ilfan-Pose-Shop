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
    cid = message.chat.id
    user_orders[cid] = {
        'video_id': message.video.file_id if message.video else message.video_note.file_id,
        'state': 'WAITING_PHOTO'
    }
    bot.send_message(cid, "🖼 Теперь пришли ФОН (скриншот или картинку):")

@bot.message_handler(content_types=['photo'])
def handle_background(message):
    cid = message.chat.id
    if cid in user_orders and user_orders[cid].get('state') == 'WAITING_PHOTO':
        user_orders[cid]['photo_id'] = message.photo[-1].file_id
        user_orders[cid]['state'] = 'WAITING_NICKNAME'
        bot.send_message(cid, "👤 Напиши свой ник в Roblox:")
    else:
        bot.send_message(cid, "Сначала пришли видео оплаты!")

@bot.message_handler(func=lambda m: True, content_types=['text'])
def handle_all_text(message):
    cid = message.chat.id
    if cid not in user_orders:
        bot.send_message(cid, "Напиши /start, чтобы начать заказ.")
        return

    state = user_orders[cid].get('state')

    if state == 'WAITING_NICKNAME':
        user_orders[cid]['nickname'] = message.text
        user_orders[cid]['state'] = 'WAITING_CHARS'
        bot.send_message(cid, "🔢 Сколько персонажей будет в позинге? (От 1 до 10):")

    elif state == 'WAITING_CHARS':
        if message.text.isdigit():
            num = int(message.text)
            if 1 <= num <= 10:
                user_orders[cid]['chars_count'] = num
                user_orders[cid]['state'] = 'WAITING_PAYMENT'
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add("Робуксы", "мм2 годли", "Телеграм-звёзды")
                bot.send_message(cid, "💳 Выбери вид оплаты:", reply_markup=markup)
            else:
                bot.send_message(cid, f"⚠️ Больше 10 персонажей нельзя, напишите число меньше {num}")
        else:
            bot.send_message(cid, "Пожалуйста, введи число.")

    elif state == 'WAITING_PAYMENT' or message.text in ["Робуксы", "мм2 годли", "Телеграм-звёзды"]:
        choice = message.text
        if choice in ["Робуксы", "мм2 годли", "Телеграм-звёзды"]:
            user_orders[cid]['payment_method'] = choice
            if choice == "Робуксы":
                msg = "💵 Вы выбрали робуксы, пожалуйста оплатите заказ по ссылке: https://www.roblox.com/games/18925562723/"
            elif choice == "мм2 годли":
                msg = "🔪 Вы выбрали годли, пожалуйста свяжитесь с владельцем (@HokhikyanHokhikyans), чтобы оплатить заказ."
            else:
                msg = "🌟 Вы выбрали телеграм звёзды, пожалуйста оплатите заказ по этому юзернейму (@HokhikyanHokhikyans)."

            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("✅ Я ОПЛАТИЛ(А)", callback_data="confirm_pay"))
            bot.send_message(cid, msg, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "confirm_pay":
        cid = call.message.chat.id
        if cid in user_orders and 'payment_method' in user_orders[cid]:
            order = user_orders[cid]
            summary = (f"🔔 НОВЫЙ ЗАКАЗ!\n"
                       f"👤 Заказчик: {order['nickname']}\n"
                       f"👥 Кол-во персонажей: {order['chars_count']}\n"
                       f"💰 Оплата: {order['payment_method']}")
            
            # Отправляем админу
            bot.send_message(ADMIN_ID, summary)
            bot.send_video(ADMIN_ID, order['video_id'], caption="Видео оплаты")
            bot.send_photo(ADMIN_ID, order['photo_id'], caption="Фон")
            
            # Ответ клиенту
            bot.send_message(cid, "🚀 Все данные переданы! Ожидайте заказ. Владелец скоро свяжется с вами.", reply_markup=types.ReplyKeyboardRemove())
            # Очищаем данные заказа после отправки
            del user_orders[cid]
        else:
            bot.send_message(cid, "Пожалуйста, сначала заполни все данные заказа!")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
