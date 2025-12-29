import telebot
from telebot import types
import re
from gatekeeper import check_access 

# --- НАСТРОЙКИ ---
TOKEN = '8595334091:AAFWypuC7IrrUG688hIlL0Nbdq4kCDLEzXU'
ADMIN_ID = 2039589760
bot = telebot.TeleBot(TOKEN)

user_data = {}

# --- СЛОВАРЬ (Переводы для новых пунктов добавь по аналогии) ---
STRINGS = {
    "Русский": {
        "ask_lang": "🌍 Выберите язык:",
        "ask_pay": "2. Способ оплаты:",
        "pay_list": ["Робуксы 💸", "Годли 🔪", "ТГ-звёзды ⭐"],
        "ask_mat": "3. Выберите материал позинга:",
        "mat_list": ["PNG", "Просто фон"],
        "ask_bg": "4. Отправьте Фон для позинга (только картинка!):",
        "err_photo": "❌ Нужно отправить только изображение! Попробуйте снова:",
        "ask_count": "5. Кол-во персонажей (от 1 до 10):",
        "limit_err": "❌ Максимум 10 персонажей. Попробуйте снова:",
        "ask_item": "6. Что добавить в руки персонажу? (Напишите текстом):",
        "item_confirm": "✅ Вы выбрали: ",
        "ask_text": "7. В позинге будет текст или нет? (Напишите текст или 'Нет'):",
        "text_confirm": "✅ У вас в позинге будет текст: ",
        "btn_done": "Готово!!!",
        "done_msg": "✅ Ваш заказ сформирован и отправлен Ильфану!\n\n📋 **Ваша анкета:**"
    }
}

# Клонируем русский на остальные языки
for l in ["English", "Հայերեն", "日本語", "中文", "Français", "한국어", "Türkçe", "العربية", "فارسی", "Қазақша", "Italiano", "Español", "O'zbekcha", "Українська", "हिन्दी", "Кыргызча", "Tiếng Việt", "עברית", "Ελληνικά"]:
    if l not in STRINGS: STRINGS[l] = STRINGS["Русский"]

@bot.message_handler(commands=['start'])
def start(message):
    error = check_access()
    if error:
        return bot.send_message(message.chat.id, error)

    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    markup.add(*[types.KeyboardButton(l) for l in STRINGS.keys()])
    bot.send_message(message.chat.id, STRINGS["Русский"]["ask_lang"], reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in STRINGS.keys())
def set_lang(message):
    user_data[message.chat.id] = {"lang": message.text}
    lang = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for p in STRINGS[lang]["pay_list"]:
        markup.add(types.KeyboardButton(p))
    msg = bot.send_message(message.chat.id, STRINGS[lang]["ask_pay"], reply_markup=markup)
    bot.register_next_step_handler(msg, get_pay_step)

# 2. Способ оплаты -> 3. Материал
def get_pay_step(message):
    lang = user_data[message.chat.id]["lang"]
    user_data[message.chat.id]["pay"] = message.text
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for m in STRINGS[lang]["mat_list"]:
        markup.add(types.KeyboardButton(m))
    msg = bot.send_message(message.chat.id, STRINGS[lang]["ask_mat"], reply_markup=markup)
    bot.register_next_step_handler(msg, get_mat_step)

# 3. Материал -> 4. Фон (если нужен)
def get_mat_step(message):
    lang = user_data[message.chat.id]["lang"]
    user_data[message.chat.id]["mat"] = message.text
    
    if message.text == "Просто фон":
        msg = bot.send_message(message.chat.id, STRINGS[lang]["ask_bg"], reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_bg_step)
    else:
        user_data[message.chat.id]["bg_id"] = "PNG (Без фона)"
        ask_count(message)

# 4. Получение фото фона
def get_bg_step(message):
    lang = user_data[message.chat.id]["lang"]
    if message.content_type == 'photo':
        user_data[message.chat.id]["bg_id"] = message.photo[-1].file_id
        ask_count(message)
    else:
        msg = bot.send_message(message.chat.id, STRINGS[lang]["err_photo"])
        bot.register_next_step_handler(msg, get_bg_step)

# 5. Количество персонажей
def ask_count(message):
    lang = user_data[message.chat.id]["lang"]
    msg = bot.send_message(message.chat.id, STRINGS[lang]["ask_count"], reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, get_count_step)

def get_count_step(message):
    lang = user_data[message.chat.id]["lang"]
    if not message.text or not message.text.isdigit():
        msg = bot.send_message(message.chat.id, "1-10:")
        bot.register_next_step_handler(msg, get_count_step)
        return
    
    count = int(message.text)
    if count > 10:
        msg = bot.send_message(message.chat.id, STRINGS[lang]["limit_err"])
        bot.register_next_step_handler(msg, get_count_step)
        return
    
    user_data[message.chat.id]["count"] = count
    msg = bot.send_message(message.chat.id, STRINGS[lang]["ask_item"])
    bot.register_next_step_handler(msg, get_item_step)

# 6. Предмет в руках
def get_item_step(message):
    lang = user_data[message.chat.id]["lang"]
    user_data[message.chat.id]["item"] = message.text
    bot.send_message(message.chat.id, f"{STRINGS[lang]['item_confirm']}*{message.text}*", parse_mode="Markdown")
    
    msg = bot.send_message(message.chat.id, STRINGS[lang]["ask_text"])
    bot.register_next_step_handler(msg, get_text_step)

# 7. Текст в позинге
def get_text_step(message):
    lang = user_data[message.chat.id]["lang"]
    user_data[message.chat.id]["text_val"] = message.text
    bot.send_message(message.chat.id, f"{STRINGS[lang]['text_confirm']}*{message.text}*", parse_mode="Markdown")
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(STRINGS[lang]["btn_done"])
    bot.send_message(message.chat.id, "Нажмите кнопку ниже для завершения:", reply_markup=markup)

@bot.message_handler(func=lambda m: "Готово!!!" in m.text)
def final_step(message):
    cid = message.chat.id
    if cid not in user_data: return
    
    lang = user_data[cid]["lang"]
    d = user_data[cid]
    
    report = (f"👤 **Заказчик:** @{message.from_user.username}\n"
              f"💰 **Оплата:** {d['pay']}\n"
              f"📦 **Материал:** {d['mat']}\n"
              f"👥 **Количество:** {d['count']}\n"
              f"🔪 **В руках:** {d['item']}\n"
              f"📝 **Текст:** {d['text_val']}")

    # Отправляем пользователю
    bot.send_message(cid, f"{STRINGS[lang]['done_msg']}\n\n{report}", parse_mode="Markdown", reply_markup=types.ReplyKeyboardRemove())
    
    # Отправляем админу
    admin_msg = f"🔥 **НОВЫЙ ЗАКАЗ**\n\n{report}"
    if d["bg_id"] != "PNG (Без фона)":
        bot.send_photo(ADMIN_ID, d["bg_id"], caption=admin_msg, parse_mode="Markdown")
    else:
        bot.send_message(ADMIN_ID, admin_msg, parse_mode="Markdown")

bot.infinity_polling()
