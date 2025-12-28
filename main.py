import telebot
from telebot import types
import re

# --- НАСТРОЙКИ ---
TOKEN = '8595334091:AAFWypuC7IrrUG688hIlL0Nbdq4kCDLEzXU'
ADMIN_ID = 2039589760
bot = telebot.TeleBot(TOKEN)

user_data = {}

# --- ПОЛНЫЙ СЛОВАРЬ (20 ЯЗЫКОВ) ---
STRINGS = {
    "Русский": {
        "ask_nick": "1. Напишите ваш ник в Roblox (только английские буквы):",
        "bad_nick": "❌ Ошибка! Используйте только английские буквы:",
        "ask_pay": "2. Способ оплаты:",
        "pay_list": ["Робуксы 💸", "Годли 🔪", "ТГ-звёзды ⭐"],
        "ask_bg": "Отправьте пожалуйста фон для позинга",
        "err_photo": "❌ Бот принимает исключительно только изображение! Пожалуйста, отправьте фото:",
        "ask_mat": "4. Материал (PNG/Обычный):",
        "ask_count": "5. Кол-во персонажей (1-10):",
        "wrong_count": "❌ Только от 1 до 10!",
        "done": "✅ Заказ отправлен Ильфану!"
    },
    "English": {
        "ask_nick": "1. Write your Roblox nickname (English letters only):",
        "bad_nick": "❌ Error! Use only English letters:",
        "ask_pay": "2. Payment method:",
        "pay_list": ["Robux 💸", "Godly 🔪", "TG-Stars ⭐"],
        "ask_bg": "Please send the background for posing",
        "err_photo": "❌ The bot exclusively accepts only images! Send a photo:",
        "ask_mat": "4. Material (PNG/Regular):",
        "ask_count": "5. Characters (1-10):",
        "wrong_count": "❌ Only 1 to 10!",
        "done": "✅ Order sent!"
    },
    "Հայերեն": {
        "ask_nick": "1. Գրեք ձեր Roblox նիկը (միայն անգլերեն տառերով).",
        "bad_nick": "❌ Սխալ: Օգտագործեք միայն անգլերեն տառեր.",
        "ask_pay": "2. Վճարման եղանակը.",
        "pay_list": ["Robux 💸", "Godly 🔪", "TG-Աստղեր ⭐"],
        "ask_bg": "Ուղարկեք լուսանկար ֆոնի համար",
        "err_photo": "❌ Բոտը ընդունում է բացառապես միայն պատկերներ: Խնդրում ենք ուղարկել լուսանկար.",
        "ask_mat": "4. Տեսակը (PNG/Սովորական).",
        "ask_count": "5. Քանակը (1-10).",
        "wrong_count": "❌ 1-ից 10-ը.",
        "done": "✅ Պատվերը ուղարկված է:"
    },
    "日本語": { "ask_nick": "1. Roblox名 (英字のみ):", "bad_nick": "❌ 英字のみを使用してください:", "ask_pay": "2. 支払い:", "pay_list": ["Robux 💸", "Godly 🔪", "TGスター ⭐"], "ask_bg": "ポージング用の背景を送信してください", "err_photo": "❌ 画像のみ受け付けます！写真を送信してください:", "ask_mat": "4. 素材 (PNG/通常):", "ask_count": "5. キャラ数 (1-10):", "wrong_count": "❌ 1-10まで!", "done": "✅ 送信完了!" },
    "中文": { "ask_nick": "1. Roblox 昵称 (仅限英文):", "bad_nick": "❌ 仅限英文:", "ask_pay": "2. 付款:", "pay_list": ["Robux 💸", "Godly 🔪", "TG星 ⭐"], "ask_bg": "请发送背景图片", "err_photo": "❌ 仅接受图片！请发送照片:", "ask_mat": "4. 材质 (PNG/常规):", "ask_count": "5. 数量 (1-10):", "wrong_count": "❌ 1到10!", "done": "✅ 已发送!" },
    "Français": { "ask_nick": "1. Nom Roblox (lettres anglaises uniquement):", "bad_nick": "❌ Erreur ! Lettres anglaises uniquement:", "ask_pay": "2. Paiement:", "pay_list": ["Robux 💸", "Godly 🔪", "Stars TG ⭐"], "ask_bg": "Veuillez envoyer le fond pour le posing", "err_photo": "❌ Uniquement des images ! Envoyez une photo:", "ask_mat": "4. Matériel (PNG/Normal):", "ask_count": "5. Nombre (1-10):", "wrong_count": "❌ 1 à 10!", "done": "✅ Envoyé!" },
    "한국어": { "ask_nick": "1. 로블록스 닉네임 (영문만):", "bad_nick": "❌ 영문만 사용 가능:", "ask_pay": "2. 결제:", "pay_list": ["로벅스 💸", "갓리 🔪", "TG 스타 ⭐"], "ask_bg": "포즈 배경을 보내주세요", "err_photo": "❌ 이미지만 가능합니다! 사진을 보내주세요:", "ask_mat": "4. 재질 (PNG/일반):", "ask_count": "5. 수 (1-10):", "wrong_count": "❌ 1~10만 가능!", "done": "✅ 전송됨!" },
    "Türkçe": { "ask_nick": "1. Roblox adı (sadece İngilizce):", "bad_nick": "❌ Sadece İngilizce harfler:", "ask_pay": "2. Ödeme:", "pay_list": ["Robux 💸", "Godly 🔪", "TG-Yıldız ⭐"], "ask_bg": "Lütfen poz için arka planı gönderin", "err_photo": "❌ Sadece resim kabul edilir! Fotoğraf gönderin:", "ask_mat": "4. Materyal (PNG/Normal):", "ask_count": "5. Sayı (1-10):", "wrong_count": "❌ 1-10 arası!", "done": "✅ Gönderildi!" },
    "العربية": { "ask_nick": "1. اسم روبلوكس (بالانجليزية فقط):", "bad_nick": "❌ الانجليزية فقط:", "ask_pay": "2. الدفع:", "pay_list": ["روبوكس 💸", "غودلي 🔪", "نجوم ⭐"], "ask_bg": "يرجى إرسال صورة الخلفية", "err_photo": "❌ الصور فقط! أرسل صورة:", "ask_mat": "4. المادة (PNG/عادي):", "ask_count": "5. العدد (1-10):", "wrong_count": "❌ 1-10 فقط!", "done": "✅ تم الإرسال!" },
    "فارسی": { "ask_nick": "1. نام روبلاکس (فقط انگلیسی):", "bad_nick": "❌ فقط حروف انگلیسی:", "ask_pay": "2. پرداخت:", "pay_list": ["روباکس 💸", "گادلی 🔪", "ستاره ⭐"], "ask_bg": "لطفا عکس پس‌زمینه را بفرستید", "err_photo": "❌ فقط عکس قبول است! تصویر بفرستید:", "ask_mat": "4. متریال (PNG/معمولی):", "ask_count": "5. تعداد (۱-۱۰):", "wrong_count": "❌ ۱ تا ۱۰!", "done": "✅ ارسال شد!" },
    "Қазақша": { "ask_nick": "1. Roblox нигі (тек ағылшынша):", "bad_nick": "❌ Тек ағылшын әріптері:", "ask_pay": "2. Төлем:", "pay_list": ["Робукс 💸", "Годли 🔪", "Жұлдыз ⭐"], "ask_bg": "Позинг үшін фон жіберіңіз", "err_photo": "❌ Тек сурет қабылданады! Фото жіберіңіз:", "ask_mat": "4. Материал (PNG/Қалыпты):", "ask_count": "5. Саны (1-10):", "wrong_count": "❌ 1-10 дейін!", "done": "✅ Жіберілді!" },
    "Italiano": { "ask_nick": "1. Nick Roblox (solo inglese):", "bad_nick": "❌ Solo lettere inglesi:", "ask_pay": "2. Pagamento:", "pay_list": ["Robux 💸", "Godly 🔪", "Stelle TG ⭐"], "ask_bg": "Invia lo sfondo per il posing", "err_photo": "❌ Solo immagini! Invia una foto:", "ask_mat": "4. Materiale (PNG/Normale):", "ask_count": "5. Personaggi (1-10):", "wrong_count": "❌ Da 1 a 10!", "done": "✅ Inviato!" },
    "Español": { "ask_nick": "1. Nick Roblox (solo inglés):", "bad_nick": "❌ Solo letras inglesas:", "ask_pay": "2. Pago:", "pay_list": ["Robux 💸", "Godly 🔪", "Estrellas ⭐"], "ask_bg": "Envía el fondo para el posing", "err_photo": "❌ ¡Solo imágenes! Envía una foto:", "ask_mat": "4. Material (PNG/Normal):", "ask_count": "5. Cantidad (1-10):", "wrong_count": "❌ 1 a 10!", "done": "✅ Enviado!" },
    "O'zbekcha": { "ask_nick": "1. Roblox niki (faqat inglizcha):", "bad_nick": "❌ Faqat ingliz harflari:", "ask_pay": "2. To'lov:", "pay_list": ["Robux 💸", "Godli 🔪", "Yulduz ⭐"], "ask_bg": "Posing uchun fon yuboring", "err_photo": "❌ Faqat rasm qabul qilinadi! Foto yuboring:", "ask_mat": "4. Material (PNG/Oddiy):", "ask_count": "5. Soni (1-10):", "wrong_count": "❌ 1-10 gacha!", "done": "✅ Yuborildi!" },
    "Українська": { "ask_nick": "1. Нік Roblox (тільки англійська):", "bad_nick": "❌ Тільки англійські літери:", "ask_pay": "2. Оплата:", "pay_list": ["Робукси 💸", "Годлі 🔪", "Зірки ⭐"], "ask_bg": "Надішліть будь ласка фон для позингу", "err_photo": "❌ Тільки фото! Надішліть зображення:", "ask_mat": "4. Матеріал (PNG/Звичайний):", "ask_count": "5. Кількість (1-10):", "wrong_count": "❌ Від 1 до 10!", "done": "✅ Відправлено!" },
    "हिन्दी": { "ask_nick": "1. रोब्लॉक्स उपनाम (केवल अंग्रेजी):", "bad_nick": "❌ केवल अंग्रेजी अक्षर:", "ask_pay": "2. भुगतान:", "pay_list": ["रोबक्स 💸", "गॉडली 🔪", "सितारे ⭐"], "ask_bg": "पोज़िंग के लिए पृष्ठभूमि भेजें", "err_photo": "❌ केवल चित्र! फोटो भेजें:", "ask_mat": "4. सामग्री (PNG/सामान्य):", "ask_count": "5. संख्या (1-10):", "wrong_count": "❌ 1 से 10 तक!", "done": "✅ भेज दिया!" },
    "Кыргызча": { "ask_nick": "1. Roblox ниги (англисче гана):", "bad_nick": "❌ Англисче гана:", "ask_pay": "2. Төлөм:", "pay_list": ["Робукс 💸", "Годли 🔪", "Жылдыз ⭐"], "ask_bg": "Позинг үчүн фон жөнөтүңүз", "err_photo": "❌ Сүрөт гана кабыл алынат! Сүрөт жөнөтүңүз:", "ask_mat": "4. Материал (PNG/Жөнөкөй):", "ask_count": "5. Саны (1-10):", "wrong_count": "❌ 1-10 гана!", "done": "✅ Жиберилди!" },
    "Tiếng Việt": { "ask_nick": "1. Tên Roblox (chỉ tiếng Anh):", "bad_nick": "❌ Chỉ dùng chữ cái tiếng Anh:", "ask_pay": "2. Thanh toán:", "pay_list": ["Robux 💸", "Godly 🔪", "Sao ⭐"], "ask_bg": "Vui lòng gửi ảnh nền posing", "err_photo": "❌ Chỉ nhận ảnh! Vui lòng gửi hình:", "ask_mat": "4. Chất liệu (PNG/Thường):", "ask_count": "5. Số lượng (1-10):", "wrong_count": "❌ 1 đến 10!", "done": "✅ Đã gửi!" },
    "עברית": { "ask_nick": "1. כינוי רובלוקס (אנגלית בלבד):", "bad_nick": "❌ אותיות באנגלית בלבד:", "ask_pay": "2. תשלום:", "pay_list": ["רובאקס 💸", "גודלי 🔪", "כוכבים ⭐"], "ask_bg": "אנא שלח רקע לפוזינג", "err_photo": "❌ תמונות בלבד! שלח תמונה:", "ask_mat": "4. חומר (PNG/רגיל):", "ask_count": "5. כמות (1-10):", "wrong_count": "❌ 1 עד 10!", "done": "✅ נשלח!" },
    "Ελληνικά": { "ask_nick": "1. Όνομα Roblox (μόνο αγγλικά):", "bad_nick": "❌ Μόνο αγγλικά γράμματα:", "ask_pay": "2. Πληρωμή:", "pay_list": ["Robux 💸", "Godly 🔪", "Αστέρια ⭐"], "ask_bg": "Στείλτε φόντο για ποζάρισμα", "err_photo": "❌ Μόνο εικόνες! Στείλτε φωτό:", "ask_mat": "4. Υλικό (PNG/Κανονικό):", "ask_count": "5. Αριθμός (1-10):", "wrong_count": "❌ 1 έως 10!", "done": "✅ Στάλθηκε!" }
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
    nick = message.text
    # РЕГУЛЯРКА: только A-Z, a-z, 0-9 и _
    if not re.match(r"^[A-Za-z0-9_]+$", nick):
        msg = bot.send_message(message.chat.id, STRINGS[lang]["bad_nick"])
        bot.register_next_step_handler(msg, get_nick)
        return
    user_data[message.chat.id]["nick"] = nick
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for p in STRINGS[lang]["pay_list"]:
        markup.add(types.KeyboardButton(p))
    msg = bot.send_message(message.chat.id, STRINGS[lang]["ask_pay"], reply_markup=markup)
    bot.register_next_step_handler(msg, get_pay)

def get_pay(message):
    lang = user_data[message.chat.id]["lang"]
    user_data[message.chat.id]["pay"] = message.text
    msg = bot.send_message(message.chat.id, STRINGS[lang]["ask_bg"], reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, get_bg)

def get_bg(message):
    lang = user_data[message.chat.id]["lang"]
    # ФИЛЬТР: ТОЛЬКО ИЗОБРАЖЕНИЕ
    if message.content_type != 'photo':
        msg = bot.send_message(message.chat.id, STRINGS[lang]["err_photo"])
        bot.register_next_step_handler(msg, get_bg)
        return
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
        msg = bot.send_message(message.chat.id, STRINGS[lang]["wrong_count"])
        bot.register_next_step_handler(msg, get_count)
        return
    d = user_data[message.chat.id]
    bot.send_message(message.chat.id, STRINGS[lang]["done"])
    # ОТЧЕТ АДМИНУ
    report = (f"🔥 **НОВЫЙ ЗАКАЗ**\n\n🌍 Язык: {d['lang']}\n🎮 Ник: `{d['nick']}`\n💰 Оплата: {d['pay']}\n"
              f"📦 Тип: {d['mat']}\n👥 Кол-во: {message.text}\n👤 От: @{message.from_user.username}")
    bot.send_photo(ADMIN_ID, d["bg_id"], caption=report, parse_mode="Markdown")

bot.infinity_polling()
