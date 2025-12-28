import telebot
from telebot import types

# --- НАСТРОЙКИ ---
TOKEN = '8595334091:AAFWypuC7IrrUG688hIlL0Nbdq4kCDLEzXU'
ADMIN_ID = 2039589760
bot = telebot.TeleBot(TOKEN)

user_data = {}

# --- СЛОВАРЬ (20 ЯЗЫКОВ) ---
STRINGS = {
    "Русский": {
        "ask_nick": "1. Напишите ник в Roblox:", "pay_list": ["Робуксы 💸", "Годли 🔪", "ТГ-звёзды ⭐"],
        "ask_pay": "2. Способ оплаты:", "ask_bg": "3. ОТПРАВЬТЕ ФОТО (Изображение) для фона:", "ask_mat": "4. Материал (PNG/Обычный):",
        "ask_count": "5. Кол-во персонажей (1-10):", "wrong": "❌ От 1 до 10!", "done": "✅ Заказ отправлен!", "err_photo": "❌ Это не фото! Пожалуйста, отправьте ИЗОБРАЖЕНИЕ:"
    },
    "English": {
        "ask_nick": "1. Roblox nickname:", "pay_list": ["Robux 💸", "Godly 🔪", "TG-Stars ⭐"],
        "ask_pay": "2. Payment:", "ask_bg": "3. SEND PHOTO for background:", "ask_mat": "4. Material (PNG/Regular):",
        "ask_count": "5. Characters (1-10):", "wrong": "❌ 1 to 10 only!", "done": "✅ Order sent!", "err_photo": "❌ Not a photo! Please send an IMAGE:"
    },
    "Հայերեն": {
        "ask_nick": "1. Roblox նիկը.", "pay_list": ["Robux 💸", "Godly 🔪", "TG-Աստղեր ⭐"],
        "ask_pay": "2. Վճարման ձևը.", "ask_bg": "3. Ուղարկեք ՖՈՏՈ ֆոնի համար.", "ask_mat": "4. Տեսակը (PNG/Սովորական).",
        "ask_count": "5. Քանակը (1-10).", "wrong": "❌ 1-ից 10-ը.", "done": "✅ Ուղարկված է.", "err_photo": "❌ Սա լուսանկար չէ: Խնդրում ենք ուղարկել ՆԿԱՐ:"
    },
    "日本語": { "ask_nick": "1. Roblox名:", "pay_list": ["Robux 💸", "Godly 🔪", "TGスター ⭐"], "ask_pay": "2. 支払い:", "ask_bg": "3. 背景の写真を送ってください:", "ask_mat": "4. 素材 (PNG/通常):", "ask_count": "5. 数 (1-10):", "wrong": "❌ 1-10まで!", "done": "✅ 送信!", "err_photo": "❌ 写真ではありません！画像を送信してください:" },
    "中文": { "ask_nick": "1. Roblox 昵称:", "pay_list": ["Robux 💸", "Godly 🔪", "TG星 ⭐"], "ask_pay": "2. 付款方式:", "ask_bg": "3. 请发送背景照片:", "ask_mat": "4. 材质 (PNG/常规):", "ask_count": "5. 数量 (1-10):", "wrong": "❌ 1到10!", "done": "✅ 已发送!", "err_photo": "❌ 不是照片！请发送图片:" },
    "Français": { "ask_nick": "1. Nom Roblox:", "pay_list": ["Robux 💸", "Godly 🔪", "Stars TG ⭐"], "ask_pay": "2. Paiement:", "ask_bg": "3. Envoyez une PHOTO pour le fond:", "ask_mat": "4. Matériel (PNG/Normal):", "ask_count": "5. Personnages (1-10):", "wrong": "❌ 1 à 10!", "done": "✅ Envoyé!", "err_photo": "❌ Pas une photo ! Envoyez une IMAGE:" },
    "한국어": { "ask_nick": "1. 로블록스 닉네임:", "pay_list": ["로벅스 💸", "갓리 🔪", "TG 스타 ⭐"], "ask_pay": "2. 결제:", "ask_bg": "3. 배경 사진을 보내주세요:", "ask_mat": "4. 재질 (PNG/일반):", "ask_count": "5. 인원 (1-10):", "wrong": "❌ 1-10!", "done": "✅ 완료!", "err_photo": "❌ 사진이 아닙니다! 이미지를 보내주세요:" },
    "Türkçe": { "ask_nick": "1. Roblox adı:", "pay_list": ["Robux 💸", "Godly 🔪", "TG-Yıldız ⭐"], "ask_pay": "2. Ödeme:", "ask_bg": "3. Arka plan FOTOĞRAFI gönderin:", "ask_mat": "4. Materyal (PNG/Normal):", "ask_count": "5. Karakter (1-10):", "wrong": "❌ 1-10!", "done": "✅ Gönderildi!", "err_photo": "❌ Fotoğraf değil! Lütfen GÖRSEL gönderin:" },
    "العربية": { "ask_nick": "1. اسم روبلوكس:", "pay_list": ["روبوكس 💸", "غودلي 🔪", "نجوم ⭐"], "ask_pay": "2. الدفع:", "ask_bg": "3. أرسل صورة للخلفية:", "ask_mat": "4. المادة (PNG/عادي):", "ask_count": "5. العدد (1-10):", "wrong": "❌ 1-10 فقط!", "done": "✅ تم الإرسال!", "err_photo": "❌ ليست صورة! يرجى إرسال صورة:" },
    "فارسی": { "ask_nick": "1. نام روبلاکس:", "pay_list": ["روباکس 💸", "گادلی 🔪", "ستاره ⭐"], "ask_pay": "2. پرداخت:", "ask_bg": "3. عکس پس‌زمینه را بفرستید:", "ask_mat": "4. متریال (PNG/معمولی):", "ask_count": "5. تعداد (۱-۱۰):", "wrong": "❌ ۱ تا ۱۰!", "done": "✅ ارسال شد!", "err_photo": "❌ عکس نیست! لطفا تصویر بفرستید:" },
    "Қазақша": { "ask_nick": "1. Roblox нигі:", "pay_list": ["Робукс 💸", "Годли 🔪", "Жұлдыз ⭐"], "ask_pay": "2. Төлем:", "ask_bg": "3. Фон үшін ФОТО жіберіңіз:", "ask_mat": "4. Материал (PNG/Қалыпты):", "ask_count": "5. Саны (1-10):", "wrong": "❌ 1-ден 10-ға дейін!", "done": "✅ Жіберілді!", "err_photo": "❌ Фото емес! Сурет жіберіңіз:" },
    "Italiano": { "ask_nick": "1. Nick Roblox:", "pay_list": ["Robux 💸", "Godly 🔪", "Stelle TG ⭐"], "ask_pay": "2. Pagamento:", "ask_bg": "3. Invia una FOTO per lo sfondo:", "ask_mat": "4. Materiale (PNG/Normale):", "ask_count": "5. Personaggi (1-10):", "wrong": "❌ Da 1 a 10!", "done": "✅ Inviato!", "err_photo": "❌ Non è una foto! Invia un'IMMAGINE:" },
    "Español": { "ask_nick": "1. Nick Roblox:", "pay_list": ["Robux 💸", "Godly 🔪", "Estrellas ⭐"], "ask_pay": "2. Pago:", "ask_bg": "3. Envía una FOTO para el fondo:", "ask_mat": "4. Material (PNG/Normal):", "ask_count": "5. Personajes (1-10):", "wrong": "❌ 1 a 10!", "done": "✅ Enviado!", "err_photo": "❌ ¡No es una foto! Envía una IMAGEN:" },
    "O'zbekcha": { "ask_nick": "1. Roblox niki:", "pay_list": ["Robux 💸", "Godli 🔪", "Yulduz ⭐"], "ask_pay": "2. To'lov:", "ask_bg": "3. Fon uchun FOTO yuboring:", "ask_mat": "4. Material (PNG/Oddiy):", "ask_count": "5. Soni (1-10):", "wrong": "❌ 1 dan 10 gacha!", "done": "✅ Yuborildi!", "err_photo": "❌ Foto emas! Rasm yuboring:" },
    "Українська": { "ask_nick": "1. Нік Roblox:", "pay_list": ["Робукси 💸", "Годлі 🔪", "ТГ-Зірки ⭐"], "ask_pay": "2. Оплата:", "ask_bg": "3. Надішліть ФОТО для фону:", "ask_mat": "4. Матеріал (PNG/Звичайний):", "ask_count": "5. Кількість (1-10):", "wrong": "❌ Від 1 до 10!", "done": "✅ Відправлено!", "err_photo": "❌ Це не фото! Надішліть ЗОБРАЖЕННЯ:" },
    "हिन्दी": { "ask_nick": "1. रोब्लॉक्स उपनाम:", "pay_list": ["रोबक्स 💸", "गॉडली 🔪", "सितारे ⭐"], "ask_pay": "2. भुगतान:", "ask_bg": "3. पृष्ठभूमि के लिए फोटो भेजें:", "ask_mat": "4. सामग्री (PNG/सामान्य):", "ask_count": "5. संख्या (1-10):", "wrong": "❌ 1 से 10!", "done": "✅ भेज दिया!", "err_photo": "❌ फोटो नहीं है! कृपया चित्र भेजें:" },
    "Кыргызча": { "ask_nick": "1. Roblox ниги:", "pay_list": ["Робукс 💸", "Годли 🔪", "Жылдыз ⭐"], "ask_pay": "2. Төлөм:", "ask_bg": "3. Фон үчүн СҮРӨТ жөнөтүңүз:", "ask_mat": "4. Материал (PNG/Жөнөкөй):", "ask_count": "5. Саны (1-10):", "wrong": "❌ 1ден 10го чейин!", "done": "✅ Жиберилди!", "err_photo": "❌ Сүрөт эмес! Сурет жөнөтүңүз:" },
    "Tiếng Việt": { "ask_nick": "1. Tên Roblox:", "pay_list": ["Robux 💸", "Godly 🔪", "Sao TG ⭐"], "ask_pay": "2. Thanh toán:", "ask_bg": "3. Gửi ẢNH làm nền:", "ask_mat": "4. Chất liệu (PNG/Thường):", "ask_count": "5. Số lượng (1-10):", "wrong": "❌ 1 đến 10!", "done": "✅ Đã gửi!", "err_photo": "❌ Không phải ảnh! Vui lòng gửi HÌNH ẢNH:" },
    "עברית": { "ask_nick": "1. כינוי רובלוקס:", "pay_list": ["רובאקס 💸", "גודלי 🔪", "כוכבים ⭐"], "ask_pay": "2. תשלום:", "ask_bg": "3. שלח תמונה לרקע:", "ask_mat": "4. חומר (PNG/רגיל):", "ask_count": "5. דמויות (1-10):", "wrong": "❌ 1 עד 10!", "done": "✅ נשלח!", "err_photo": "❌ לא תמונה! שלח תמונה:" },
    "Ελληνικά": { "ask_nick": "1. Όνομα Roblox:", "pay_list": ["Robux 💸", "Godly 🔪", "Αστέρια ⭐"], "ask_pay": "2. Πληρωμή:", "ask_bg": "3. Στείλτε ΦΩΤΟΓΡΑΦΙΑ για φόντο:", "ask_mat": "4. Υλικό (PNG/Κανονικό):", "ask_count": "5. Χαρακτήρες (1-10):", "wrong": "❌ 1 έως 10!", "done": "✅ Στάλθηκε!", "err_photo": "❌ Δεν είναι φωτογραφία! Στείλτε ΕΙΚΟΝΑ:" }
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    markup.add(*[types.KeyboardButton(l) for l in STRINGS.keys()])
    bot.send_message(message.chat.id, "🌍 Select Language / Выберите язык:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in STRINGS.keys())
def set_lang(message):
    user_data[message.chat.id] = {"lang": message.text}
    msg = bot.send_message(message.chat.id, STRINGS[message.text]["ask_nick"], reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, get_nick)

def get_nick(message):
    lang = user_data[message.chat.id]["lang"]
    user_data[message.chat.id]["nick"] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*[types.KeyboardButton(p) for p in STRINGS[lang]["pay_list"]])
    msg = bot.send_message(message.chat.id, STRINGS[lang]["ask_pay"], reply_markup=markup)
    bot.register_next_step_handler(msg, get_pay)

def get_pay(message):
    lang = user_data[message.chat.id]["lang"]
    user_data[message.chat.id]["pay"] = message.text
    msg = bot.send_message(message.chat.id, STRINGS[lang]["ask_bg"], reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, get_bg)

def get_bg(message):
    lang = user_data[message.chat.id]["lang"]
    # ФИКС БАГА: Проверка на тип контента
    if message.content_type != 'photo':
        msg = bot.send_message(message.chat.id, STRINGS[lang]["err_photo"])
        bot.register_next_step_handler(msg, get_bg)
        return
    
    # Сохраняем самое качественное фото
    user_data[message.chat.id]["bg_id"] = message.photo[-1].file_id
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("PNG", "Regular")
    msg = bot.send_message(message.chat.id, STRINGS[lang]["ask_mat"], reply_markup=markup)
    bot.register_next_step_handler(msg, get_mat)

def get_mat(message):
    lang = user_data[message.chat.id]["lang"]
    user_data[message.chat.id]["mat"] = message.text
    msg = bot.send_message(message.chat.id, STRINGS[lang]["ask_count"])
    bot.register_next_step_handler(msg, get_count)

def get_count(message):
    lang = user_data[message.chat.id]["lang"]
    if not message.text.isdigit() or not (1 <= int(message.text) <= 10):
        msg = bot.send_message(message.chat.id, STRINGS[lang]["wrong"])
        bot.register_next_step_handler(msg, get_count)
        return
    
    d = user_data[message.chat.id]
    bot.send_message(message.chat.id, STRINGS[lang]["done"])
    
    # ОТПРАВКА АДМИНУ (ФОТО + ТЕКСТ)
    report = (f"🆕 **НОВЫЙ ЗАКАЗ**\n\n"
              f"🌍 Язык: {d['lang']}\n"
              f"🎮 Roblox: `{d['nick']}`\n"
              f"💰 Оплата: {d['pay']}\n"
              f"📦 Тип: {d['mat']}\n"
              f"👥 Кол-во: {message.text}\n"
              f"👤 От: @{message.from_user.username}")
    
    bot.send_photo(ADMIN_ID, d["bg_id"], caption=report, parse_mode="Markdown")

bot.infinity_polling()
