import telebot
from telebot import types

TOKEN = '8595334091:AAFWypuC7IrrUG688hIlL0Nbdq4kCDLEzXU'
ADMIN_ID = 2039589760
bot = telebot.TeleBot(TOKEN)

user_data = {}

# --- ПОЛНЫЙ СЛОВАРЬ (20 ЯЗЫКОВ) ---
STRINGS = {
    "Русский": {
        "ask_nick": "1. Напишите ник в Roblox:", "pay_list": ["Робуксы 💸", "Годли 🔪", "ТГ-звёзды ⭐"],
        "ask_pay": "2. Способ оплаты:", "ask_bg": "3. Опишите фон:", "ask_mat": "4. Материал (PNG/Обычный):",
        "ask_count": "5. Кол-во персонажей (1-10):", "wrong": "❌ От 1 до 10!", "done": "✅ Заказ отправлен!"
    },
    "English": {
        "ask_nick": "1. Roblox nickname:", "pay_list": ["Robux 💸", "Godly 🔪", "TG-Stars ⭐"],
        "ask_pay": "2. Payment:", "ask_bg": "3. Background:", "ask_mat": "4. Material (PNG/Regular):",
        "ask_count": "5. Characters (1-10):", "wrong": "❌ 1 to 10 only!", "done": "✅ Order sent!"
    },
    "Հայերեն": {
        "ask_nick": "1. Roblox նիկը.", "pay_list": ["Robux 💸", "Godly 🔪", "TG-Աստղեր ⭐"],
        "ask_pay": "2. Վճարման ձևը.", "ask_bg": "3. Ֆոնը.", "ask_mat": "4. Տեսակը (PNG/Սովորական).",
        "ask_count": "5. Քանակը (1-10).", "wrong": "❌ 1-ից 10-ը.", "done": "✅ Ուղարկված է."
    },
    "日本語": {
        "ask_nick": "1. Robloxのニックネーム:", "pay_list": ["Robux 💸", "Godly 🔪", "TGスター ⭐"],
        "ask_pay": "2. 支払い方法:", "ask_bg": "3. 背景の説明:", "ask_mat": "4. 素材 (PNG/通常):",
        "ask_count": "5. キャラクター数 (1-10):", "wrong": "❌ 1から10まで！", "done": "✅ 送信されました！"
    },
    "中文": {
        "ask_nick": "1. Roblox 昵称:", "pay_list": ["Robux 💸", "Godly 🔪", "TG星 ⭐"],
        "ask_pay": "2. 付款方式:", "ask_bg": "3. 背景描述:", "ask_mat": "4. 材质 (PNG/常规):",
        "ask_count": "5. 角色数量 (1-10):", "wrong": "❌ 仅限 1 到 10！", "done": "✅ 订单已发送！"
    },
    "Français": {
        "ask_nick": "1. Nom Roblox:", "pay_list": ["Robux 💸", "Godly 🔪", "Étoiles TG ⭐"],
        "ask_pay": "2. Paiement:", "ask_bg": "3. Fond:", "ask_mat": "4. Matériel (PNG/Normal):",
        "ask_count": "5. Personnages (1-10):", "wrong": "❌ De 1 à 10!", "done": "✅ Envoyé!"
    },
    "한국어": {
        "ask_nick": "1. 로블록스 닉네임:", "pay_list": ["로벅스 💸", "갓리 🔪", "TG 스타 ⭐"],
        "ask_pay": "2. 결제 방법:", "ask_bg": "3. 배경 설명:", "ask_mat": "4. 재질 (PNG/일반):",
        "ask_count": "5. 캐릭터 수 (1-10):", "wrong": "❌ 1에서 10까지만!", "done": "✅ 전송 완료!"
    },
    "Türkçe": {
        "ask_nick": "1. Roblox adı:", "pay_list": ["Robux 💸", "Godly 🔪", "TG-Yıldızları ⭐"],
        "ask_pay": "2. Ödeme:", "ask_bg": "3. Arka plan:", "ask_mat": "4. Materyal (PNG/Normal):",
        "ask_count": "5. Karakter (1-10):", "wrong": "❌ 1-10 arası!", "done": "✅ Gönderildi!"
    },
    "العربية": {
        "ask_nick": "1. اسم روبلوكس:", "pay_list": ["روبوكس 💸", "غودلي 🔪", "نجوم ⭐"],
        "ask_pay": "2. الدفع:", "ask_bg": "3. الخلفية:", "ask_mat": "4. المادة (PNG/عادي):",
        "ask_count": "5. عدد الشخصيات (1-10):", "wrong": "❌ 1-10 فقط!", "done": "✅ تم الإرسال!"
    },
    "فارسی": {
        "ask_nick": "1. نام روبلاکس:", "pay_list": ["روباکس 💸", "گادلی 🔪", "ستاره ⭐"],
        "ask_pay": "2. پرداخت:", "ask_bg": "3. پس‌زمینه:", "ask_mat": "4. متریال (PNG/معمولی):",
        "ask_count": "5. تعداد (۱-۱۰):", "wrong": "❌ فقط ۱ تا ۱۰!", "done": "✅ ارسال شد!"
    },
    "Қазақша": {
        "ask_nick": "1. Roblox нигі:", "pay_list": ["Робукс 💸", "Годли 🔪", "ТГ-Жұлдыз ⭐"],
        "ask_pay": "2. Төлем:", "ask_bg": "3. Фон:", "ask_mat": "4. Материал (PNG/Қалыпты):",
        "ask_count": "5. Саны (1-10):", "wrong": "❌ 1-ден 10-ға дейін!", "done": "✅ Жіберілді!"
    },
    "Italiano": {
        "ask_nick": "1. Nick Roblox:", "pay_list": ["Robux 💸", "Godly 🔪", "Stelle TG ⭐"],
        "ask_pay": "2. Pagamento:", "ask_bg": "3. Sfondo:", "ask_mat": "4. Materiale (PNG/Normale):",
        "ask_count": "5. Personaggi (1-10):", "wrong": "❌ Da 1 a 10!", "done": "✅ Inviato!"
    },
    "Español": {
        "ask_nick": "1. Nick Roblox:", "pay_list": ["Robux 💸", "Godly 🔪", "Estrellas TG ⭐"],
        "ask_pay": "2. Pago:", "ask_bg": "3. Fondo:", "ask_mat": "4. Material (PNG/Normal):",
        "ask_count": "5. Personajes (1-10):", "wrong": "❌ ¡Solo 1 a 10!", "done": "✅ ¡Enviado!"
    },
    "O'zbekcha": {
        "ask_nick": "1. Roblox niki:", "pay_list": ["Robux 💸", "Godli 🔪", "TG-Yulduz ⭐"],
        "ask_pay": "2. To'lov:", "ask_bg": "3. Fon:", "ask_mat": "4. Material (PNG/Oddiy):",
        "ask_count": "5. Soni (1-10):", "wrong": "❌ 1 dan 10 gacha!", "done": "✅ Yuborildi!"
    },
    "Українська": {
        "ask_nick": "1. Нік Roblox:", "pay_list": ["Робукси 💸", "Годлі 🔪", "ТГ-Зірки ⭐"],
        "ask_pay": "2. Оплата:", "ask_bg": "3. Фон:", "ask_mat": "4. Матеріал (PNG/Звичайний):",
        "ask_count": "5. Кількість (1-10):", "wrong": "❌ Від 1 до 10!", "done": "✅ Відправлено!"
    },
    "हिन्दी": {
        "ask_nick": "1. रोब्लॉक्स उपनाम:", "pay_list": ["रोबक्स 💸", "गॉडली 🔪", "सितारे ⭐"],
        "ask_pay": "2. भुगतान:", "ask_bg": "3. पृष्ठभूमि:", "ask_mat": "4. सामग्री (PNG/सामान्य):",
        "ask_count": "5. पात्र (1-10):", "wrong": "❌ केवल 1 से 10 तक!", "done": "✅ भेज दिया गया!"
    },
    "Кыргызча": {
        "ask_nick": "1. Roblox ниги:", "pay_list": ["Робукс 💸", "Годли 🔪", "Жылдыз ⭐"],
        "ask_pay": "2. Төлөм:", "ask_bg": "3. Фон:", "ask_mat": "4. Материал (PNG/Жөнөкөй):",
        "ask_count": "5. Саны (1-10):", "wrong": "❌ 1ден 10го чейин!", "done": "✅ Жиберилди!"
    },
    "Tiếng Việt": {
        "ask_nick": "1. Tên Roblox:", "pay_list": ["Robux 💸", "Godly 🔪", "Sao TG ⭐"],
        "ask_pay": "2. Thanh toán:", "ask_bg": "3. Nền:", "ask_mat": "4. Chất liệu (PNG/Thường):",
        "ask_count": "5. Số nhân vật (1-10):", "wrong": "❌ Chỉ từ 1 đến 10!", "done": "✅ Đã gửi!"
    },
    "עברית": {
        "ask_nick": "1. כינוי רובלוקס:", "pay_list": ["רובאקס 💸", "גודלי 🔪", "כוכבים ⭐"],
        "ask_pay": "2. תשלום:", "ask_bg": "3. רקע:", "ask_mat": "4. חומר (PNG/רגיל):",
        "ask_count": "5. דמויות (1-10):", "wrong": "❌ רק 1 עד 10!", "done": "✅ נשלח!"
    },
    "Ελληνικά": {
        "ask_nick": "1. Όνομα Roblox:", "pay_list": ["Robux 💸", "Godly 🔪", "Αστέρια ⭐"],
        "ask_pay": "2. Πληρωμή:", "ask_bg": "3. Φόντο:", "ask_mat": "4. Υλικό (PNG/Κανονικό):",
        "ask_count": "5. Χαρακτήρες (1-10):", "wrong": "❌ Μόνο 1 έως 10!", "done": "✅ Στάλθηκε!"
    }
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    markup.add(*[types.KeyboardButton(l) for l in STRINGS.keys()])
    bot.send_message(message.chat.id, "🌍 Select Language:", reply_markup=markup)

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
    user_data[message.chat.id]["bg"] = message.text
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
    report = (f"🆕 **ЗАКАЗ**\n🌍 Язык: {lang}\n🎮 Ник: `{d['nick']}`\n💰 Оплата: {d['pay']}\n"
              f"🖼 Фон: {d['bg']}\n📦 Тип: {d['mat']}\n👥 Кол-во: {message.text}\n👤 От: @{message.from_user.username}")
    bot.send_message(ADMIN_ID, report, parse_mode="Markdown")

bot.infinity_polling()
