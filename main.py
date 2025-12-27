import telebot
from telebot import types
from flask import Flask
from threading import Thread
import os

# --- Веб-сервер для Render ---
app = Flask('')
@app.route('/')
def home(): return "Бот Ильфана работает!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    Thread(target=run).start()

# --- Настройки бота ---
API_TOKEN = '8595334091:AAFWypuC7IrrUG688hIlL0Nbdq4kCDLEzXU'
ADMIN_ID = 2039589760 
bot = telebot.TeleBot(API_TOKEN)

user_orders = {}

@bot.message_handler(commands=['start'])
def start(message):
    cid = message.chat.id
    user_orders[cid] = {'state': 'SELECT_PAYMENT'}
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Робуксы", "мм2 годли", "Телеграм-звёзды")
    
    shop_link = "https://dominikanayyuhu.github.io/Ilfan-Pose-Shop/"
    bot.send_message(cid, f"👋 Привет! Магазин тут: {shop_link}\n💳 Выбери вид оплаты:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.chat.id in user_orders and user_orders[m.chat.id].get('state') == 'SELECT_PAYMENT')
def handle_payment_choice(message):
    cid = message.chat.id
    choice = message.text
    if choice in ["Робуксы", "мм2 годли", "Телеграм-звёзды"]:
        user_orders[cid]['payment_method'] = choice
        user_orders[cid]['state'] = 'WAITING_PHOTO'
        bot.send_message(cid, f"✅ Вы выбрали: {choice}.\n🖼 Теперь пришли ФОН (скриншот или картинку):", reply_markup=types.ReplyKeyboardRemove())
    else:
        bot.send_message(cid, "❌ Пожалуйста, выбери вариант из меню.")

@bot.message_handler(content_types=['photo'], func=lambda m: m.chat.id in user_orders and user_orders[m.chat.id].get('state') == 'WAITING_PHOTO')
def handle_photo(message):
    cid = message.chat.id
    user_orders[cid]['photo_id'] = message.photo[-1].file_id
    user_orders[cid]['state'] = 'WAITING_NICKNAME'
    bot.send_message(cid, "👤 Напиши свой ник в Roblox:")

@bot.message_handler(func=lambda m: m.chat.id in user_orders and user_orders[m.chat.id].get('state') == 'WAITING_NICKNAME')
def handle_nickname(message):
    cid = message.chat.id
    user_orders[cid]['nickname'] = message.text
    user_orders[cid]['state'] = 'WAITING_CHARS'
    bot.send_message(cid, "🔢 Сколько персонажей будет в позинге? (От 1 до 10):")

@bot.message_handler(func=lambda m: m.chat.id in user_orders and user_orders[m.chat.id].get('state') == 'WAITING_CHARS')
def handle_chars(message):
    cid = message.chat.id
    text = message.text
    if text.isdigit():
        num = int(text)
        if 1 <= num <= 10:
            user_orders[cid]['chars_count'] = num
            pay_method = user_orders[cid]['payment_method']
            
            if pay_method == "мм2 годли":
                # Для годли видео не нужно - сразу кнопка подтверждения
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("✅ Я ОПЛАТИЛ(А)", callback_data="confirm_pay"))
                bot.send_message(cid, "🔪 Пожалуйста, свяжитесь с владельцем (@HokhikyanHokhikyans) для передачи предметов. После этого нажмите кнопку ниже:", reply_markup=markup)
            else:
                user_orders[cid]['state'] = 'WAITING_VIDEO'
                if pay_method == "Робуксы":
                    link = "https://www.roblox.com/games/18925562723/"
                    bot.send_message(cid, f"💵 Оплатите тут: {link}\n🎬 После оплаты пришли видео-доказательство:")
                else:
                    bot.send_message(cid, "🌟 Оплатите по юзернейму @HokhikyanHokhikyans\n🎬 После оплаты пришли видео-доказательство отправки звёзд:")
        else:
            bot.send_message(cid, f"⚠️ Напишите число меньше {num}")
    else:
        bot.send_message(cid, "Пожалуйста, введи число.")

@bot.message_handler(content_types=['video', 'video_note'], func=lambda m: m.chat.id in user_orders and user_orders[m.chat.id].get('state') == 'WAITING_VIDEO')
def handle_video(message):
    cid = message.chat.id
    user_orders[cid]['video_id'] = message.video.file_id if message.video else message.video_note.file_id
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Я ОПЛАТИЛ(А)", callback_data="confirm_pay"))
    bot.send_message(cid, "Видео получено! Нажмите кнопку для завершения заказа:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "confirm_pay")
def final_step(call):
    cid = call.message.chat.id
    if cid in user_orders:
        order = user_orders[cid]
        summary = (f"🔔 НОВЫЙ ЗАКАЗ!\n"
                   f"👤 Заказчик: {order.get('nickname')}\n"
                   f"👥 Кол-во персонажей: {order.get('chars_count')}\n"
                   f"💰 Оплата: {order.get('payment_method')}")
        
        # Отправка тебе (админу)
        bot.send_message(ADMIN_ID, summary)
        bot.send_photo(ADMIN_ID, order['photo_id'], caption="Выбранный фон")
        if 'video_id' in order:
            bot.send_video(ADMIN_ID, order['video_id'], caption="Видео оплаты")
        
        # Ответ клиенту
        bot.send_message(cid, "🚀 Все данные переданы! Ожидайте заказ. Владелец скоро свяжется с вами.")
        del user_orders[cid]
        bot.answer_callback_query(call.id, "Заказ отправлен!")
    else:
        bot.send_message(cid, "Ошибка. Нажмите /start")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
