import telebot
from telebot import types
import re
from gatekeeper import check_access 

# --- НАСТРОЙКИ ---
TOKEN = '8595334091:AAFWypuC7IrrUG688hIlL0Nbdq4kCDLEzXU'
ADMIN_ID = 2039589760
bot = telebot.TeleBot(TOKEN)

user_data = {}

# --- СЛОВАРЬ ---
STRINGS = {
    "Русский": {
        "ask_nick": "1. Напишите ваш ник в Roblox (английские буквы):",
        "bad_nick": "❌ Ошибка! Используйте только английские буквы и цифры:",
        "ask_pay": "2. Способ оплаты:", "pay_list": ["Робуксы 💸", "Годли 🔪", "ТГ-звёзды ⭐"],
        "ask_mat": "3. Материал позинга:", "mat_list": ["PNG", "Просто фон"],
        "ask_bg": "4. Отправьте Фон (только картинка!):", "err_photo": "❌ Только фото!",
        "ask_count": "5. Кол-во персонажей (1-10):", "limit_err": "❌ Максимум 10!",
        "ask_item": "6. Что в руках? (Напишите):", "item_confirm": "✅ Вы выбрали: ",
        "ask_text": "7. Текст в позинге? (Напишите или 'Нет'):", "text_confirm": "✅ Текст: ",
        "btn_done": "Готово!!!", "done_msg": "✅ Заказ отправлен!"
    },
    "English": {
        "ask_nick": "1. Type your Roblox nickname (English letters only):",
        "bad_nick": "❌ Error! Use only English letters and numbers:",
        "ask_pay": "2. Payment method:", "pay_list": ["Robux 💸", "Godly 🔪", "TG Stars ⭐"],
        "ask_mat": "3. Material:", "mat_list": ["PNG", "Simple background"],
        "ask_bg": "4. Send background (image only!):", "err_photo": "❌ Image only!",
        "ask_count": "5. Characters (1-10):", "limit_err": "❌ Max 10!",
        "ask_item": "6. Item in hands? (Type it):", "item_confirm": "✅ You chose: ",
        "ask_text": "7. Text in posing? (Type or 'No'):", "text_confirm": "✅ Text: ",
        "btn_done": "Done!!!", "done_msg": "✅ Order sent!"
    }
}

# Копируем English для остальных (для безопасности)
OTHER = ["فارسی", "Türkçe", "中文", "Հայերեն", "日本語", "Français", "한국어", "العربية", "Қазақша", "Italiano", "Español", "O'zbekcha", "Українська", "हिन्दी", "Кыргызча", "Tiếng Việt", "עברית", "Ελληνικά"]
for l in OTHER:
    if l not in STRINGS: STRINGS[l] = STRINGS["English"]

@bot.message_handler(commands=['start'])
def start(message):
    error = check_access()
    if error: return bot.send_message(message.chat.id, error)
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    markup.add(*[types.KeyboardButton(l) for l in STRINGS.keys()])
    bot.send_message(message.chat.id, "🌍 Select Language / Выберите язык:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in STRINGS.keys())
def set_lang(message):
    lang = message.text
    user_data[message.chat.id] = {"lang": lang}
    # ПУНКТ 1: Запрос ника
    msg = bot.send_message(message.chat.id, STRINGS[lang]["ask_nick"], reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, get_nick_step)

def get_nick_step(message):
    lang = user_data[message.chat.id]["lang"]
    if not message.text or not re.match(r"^[A-Za-z0-9_]+$", message.text):
        msg = bot.send_message(message.chat.id, STRINGS[lang]["bad_nick"])
        bot.register_next_step_handler(msg, get_nick_step)
        return
    user_data[message.chat.id]["nick"] = message.text
    # ПУНКТ 2: Оплата
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for p in STRINGS[lang]["pay_list"]: markup.add(types.KeyboardButton(p))
    msg = bot.send_message(message.chat.id, STRINGS[lang]["ask_pay"], reply_markup=markup)
    bot.register_next_step_handler(msg, get_pay_step)

def get_pay_step(message):
    lang = user_data[message.chat.id]["lang"]
    user_data[message.chat.id]["pay"] = message.text
    # ПУНКТ 3: Материал
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for m in STRINGS[lang]["mat_list"]: markup.add(types.KeyboardButton(m))
    msg = bot.send_message(message.chat.id, STRINGS[lang]["ask_mat"], reply_markup=markup)
    bot.register_next_step_handler(msg, get_mat_step)

def get_mat_step(message):
    lang = user_data[message.chat.id]["lang"]
    mat = message.text
    user_data[message.chat.id]["mat"] = mat
    # ПУНКТ 4: Фон (проверка на разных языках)
    if mat in ["Просто фон", "Simple background", "پس‌زمینه", "Sıradan arka plan", "普通背景"]:
        msg = bot.send_message(message.chat.id, STRINGS[lang]["ask_bg"], reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_bg_step)
    else:
        user_data[message.chat.id]["bg_id"] = "PNG"
        ask_count(message)

def get_bg_step(message):
    lang = user_data[message.chat.id]["lang"]
    if message.content_type == 'photo':
        user_data[message.chat.id]["bg_id"] = message.photo[-1].file_id
        ask_count(message)
    else:
        bot.register_next_step_handler(bot.send_message(message.chat.id, STRINGS[lang]["err_photo"]), get_bg_step)

def ask_count(message):
    lang = user_data[message.chat.id]["lang"]
    msg = bot.send_message(message.chat.id, STRINGS[lang]["ask_count"], reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, get_count_step)

def get_count_step(message):
    lang = user_data[message.chat.id]["lang"]
    if not message.text or not message.text.isdigit():
        bot.register_next_step_handler(bot.send_message(message.chat.id, "1-10:"), get_count_step)
        return
    count = int(message.text)
    if count > 10:
        bot.register_next_step_handler(bot.send_message(message.chat.id, STRINGS[lang]["limit_err"]), get_count_step)
        return
    user_data[message.chat.id]["count"] = count
    # ПУНКТ 6: Предмет
    msg = bot.send_message(message.chat.id, STRINGS[lang]["ask_item"])
    bot.register_next_step_handler(msg, get_item_step)

def get_item_step(message):
    lang = user_data[message.chat.id]["lang"]
    user_data[message.chat.id]["item"] = message.text
    bot.send_message(message.chat.id, f"{STRINGS[lang]['item_confirm']}*{message.text}*", parse_mode="Markdown")
    # ПУНКТ 7: Текст
    msg = bot.send_message(message.chat.id, STRINGS[lang]["ask_text"])
    bot.register_next_step_handler(msg, get_text_step)

def get_text_step(message):
    lang = user_data[message.chat.id]["lang"]
    user_data[message.chat.id]["text_val"] = message.text
    bot.send_message(message.chat.id, f"{STRINGS[lang]['text_confirm']}*{message.text}*", parse_mode="Markdown")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(STRINGS[lang]["btn_done"])
    bot.send_message(message.chat.id, "---", reply_markup=markup)

@bot.message_handler(func=lambda m: any(word in m.text for word in ["Готово", "Done", "شد", "Tamam", "完成"]))
def final_step(message):
    cid = message.chat.id
    if cid not in user_data: return
    d = user_data[cid]
    report = (f"🎮 **Nick:** `{d['nick']}`\n"
              f"👤 **Customer:** @{message.from_user.username}\n"
              f"💰 **Pay:** {d['pay']}\n"
              f"📦 **Mat:** {d['mat']}\n"
              f"👥 **Count:** {d['count']}\n"
              f"🔪 **Item:** {d['item']}\n"
              f"📝 **Text:** {d['text_val']}")
    
    bot.send_message(cid, f"{STRINGS[d['lang']]['done_msg']}\n\n{report}", parse_mode="Markdown", reply_markup=types.ReplyKeyboardRemove())
    
    admin_msg = f"🔥 **NEW ORDER**\n\n{report}"
    if d["bg_id"] != "PNG":
        bot.send_photo(ADMIN_ID, d["bg_id"], caption=admin_msg, parse_mode="Markdown")
    else:
        bot.send_message(ADMIN_ID, admin_msg, parse_mode="Markdown")

bot.infinity_polling()
