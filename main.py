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
        "bad_nick": "❌ Ошибка! Используйте только английские буквы и цифры:",
        "ask_pay": "2. Способ оплаты:",
        "pay_list": ["Робуксы 💸", "Годли 🔪", "ТГ-звёзды ⭐"],
        "ask_bg": "Отправьте пожалуйста фон для позинга",
        "err_photo": "❌ Бот принимает исключительно только изображение! Пожалуйста, отправьте фото:",
        "ask_mat": "4. Материал (PNG/Обычный фон):",
        "ask_count": "5. Кол-во персонажей в позинге (От 1 до 10):",
        "limit_err": "Похоже вы решили добавить больше 10 персонажей, к сожелению лимит до 10 персонажей. Попробуйте снова:",
        "done": "✅ Заказ отправлен Ильфану!"
    },
    "English": {
        "ask_nick": "1. Write your Roblox nickname (English letters only):",
        "bad_nick": "❌ Error! Use only English letters and numbers:",
        "ask_pay": "2. Payment method:",
        "pay_list": ["Robux 💸", "Godly 🔪", "TG-Stars ⭐"],
        "ask_bg": "Please send the background for posing",
        "err_photo": "❌ The bot exclusively accepts only images! Send a photo:",
        "ask_mat": "4. Material (PNG/Regular background):",
        "ask_count": "5. Characters (1-10):",
        "limit_err": "It seems you decided to add more than 10 characters, unfortunately the limit is 10. Try again:",
        "done": "✅ Order sent!"
    },
    "Հայերեն": { "ask_nick": "1. Գրեք ձեր Roblox նիկը.", "bad_nick": "❌ Սխալ: Օգտագործեք անգլերեն.", "ask_pay": "2. Վճարում.", "pay_list": ["Robux 💸", "Godly 🔪", "TG-Աստղեր ⭐"], "ask_bg": "Ուղարկեք լուսանկար ֆոնի համար", "err_photo": "❌ Միայն լուսանկար:", "ask_mat": "4. Տեսակը (PNG/Սովորական).", "ask_count": "5. Քանակը (1-10).", "limit_err": "Սահմանաչափը 10 է:", "done": "✅ Ուղարկված է:" },
    "日本語": { "ask_nick": "1. Roblox名:", "bad_nick": "❌ 英字のみ:", "ask_pay": "2. 支払い:", "pay_list": ["Robux 💸", "Godly 🔪", "TGスター ⭐"], "ask_bg": "背景を送信してください", "err_photo": "❌ 写真のみ:", "ask_mat": "4. 素材 (PNG/通常):", "ask_count": "5. 数 (1-10):", "limit_err": "10人までです:", "done": "✅ 送信!" },
    "中文": { "ask_nick": "1. Roblox 昵称:", "bad_nick": "❌ 仅限英文:", "ask_pay": "2. 付款:", "pay_list": ["Robux 💸", "Godly 🔪", "TG星 ⭐"], "ask_bg": "请发送背景图片", "err_photo": "❌ 仅限图片:", "ask_mat": "4. 材质 (PNG/常规):", "ask_count": "5. 数量 (1-10):", "limit_err": "限制为 10 个角色:", "done": "✅ 已发送!" },
    "Français": { "ask_nick": "1. Nom Roblox:", "bad_nick": "❌ Lettres anglaises uniquement:", "ask_pay": "2. Paiement:", "pay_list": ["Robux 💸", "Godly 🔪", "Stars TG ⭐"], "ask_bg": "Envoyez le fond", "err_photo": "❌ Photos uniquement!", "ask_mat": "4. Matériel:", "ask_count": "5. Nombre (1-10):", "limit_err": "La limite est de 10:", "done": "✅ Envoyé!" },
    "한국어": { "ask_nick": "1. 로블록스 닉네임:", "bad_nick": "❌ 영문만:", "ask_pay": "2. 결제:", "pay_list": ["로벅스 💸", "갓리 🔪", "TG 스타 ⭐"], "ask_bg": "배경 사진을 보내주세요", "err_photo": "❌ 사진만 가능!", "ask_mat": "4. 재질:", "ask_count": "5. 수 (1-10):", "limit_err": "최대 10명:", "done": "✅ 완료!" },
    "Türkçe": { "ask_nick": "1. Roblox adı:", "bad_nick": "❌ Sadece İngilizce:", "ask_pay": "2. Ödeme:", "pay_list": ["Robux 💸", "Godly 🔪", "TG-Yıldız ⭐"], "ask_bg": "Arka planı gönderin", "err_photo": "❌ Sadece resim!", "ask_mat": "4. Materyal:", "ask_count": "5. Sayı (1-10):", "limit_err": "Limit 10 karakter:", "done": "✅ Gönderildi!" },
    "العربية": { "ask_nick": "1. اسم روبلوكس:", "bad_nick": "❌ الانجليزية فقط:", "ask_pay": "2. الدفع:", "pay_list": ["روبوكس 💸", "غودلي 🔪", "نجوم ⭐"], "ask_bg": "أرسل الخلفية", "err_photo": "❌ صور فقط!", "ask_mat": "4. المادة:", "ask_count": "5. العدد (1-10):", "limit_err": "الحد الأقصى 10:", "done": "✅ تم!" },
    "فارسی": { "ask_nick": "1. نام روبلاکس:", "bad_nick": "❌ فقط انگلیسی:", "ask_pay": "2. پرداخت:", "pay_list": ["روباکس 💸", "گادلی 🔪", "ستاره ⭐"], "ask_bg": "عکس پس‌زمینه را بفرستید", "err_photo": "❌ فقط عکس!", "ask_mat": "4. متریال:", "ask_count": "5. تعداد (۱-۱۰):", "limit_err": "حداکثر ۱۰ نفر:", "done": "✅ ارسال شد!" },
    "Қазақша": { "ask_nick": "1. Roblox нигі:", "bad_nick": "❌ Тек ағылшын әріптері:", "ask_pay": "2. Төлем:", "pay_list": ["Робукс 💸", "Годли 🔪", "Жұлдыз ⭐"], "ask_bg": "Фон жіберіңіз", "err_photo": "❌ Тек сурет!", "ask_mat": "4. Материал:", "ask_count": "5. Саны (1-10):", "limit_err": "Шектеу 10 адам:", "done": "✅ Жіберілді!" },
    "Italiano": { "ask_nick": "1. Nick Roblox:", "bad_nick": "❌ Solo lettere inglesi:", "ask_pay": "2. Pagamento:", "pay_list": ["Robux 💸", "Godly 🔪", "Stelle TG ⭐"], "ask_bg": "Invia lo sfondo", "err_photo": "❌ Solo immagini!", "ask_mat": "4. Materiale:", "ask_count": "5. Personaggi (1-10):", "limit_err": "Il limite è 10:", "done": "✅ Inviato!" },
    "Español": { "ask_nick": "1. Nick Roblox:", "bad_nick": "❌ Solo letras inglesas:", "ask_pay": "2. Pago:", "pay_list": ["Robux 💸", "Godly 🔪", "Estrellas ⭐"], "ask_bg": "Envía el fondo", "err_photo": "❌ Solo imágenes!", "ask_mat": "4. Material:", "ask_count": "5. Cantidad (1-10):", "limit_err": "Límite de 10:", "done": "✅ Enviado!" },
    "O'zbekcha": { "ask_nick": "1. Roblox niki:", "bad_nick": "❌ Faqat ingliz harflari:", "ask_pay": "2. To'lov:", "pay_list": ["Robux 💸", "Godli 🔪", "Yulduz ⭐"], "ask_bg": "Fon yuboring", "err_photo": "❌ Faqat rasm!", "ask_mat": "4. Material:", "ask_count": "5. Soni (1-10):", "limit_err": "Cheklov 10 киши:", "done": "✅ Yuborildi!" },
    "Українська": { "ask_nick": "1. Нік Roblox:", "bad_nick": "❌ Тільки англійські літери:", "ask_pay": "2. Оплата:", "pay_list": ["Робукси 💸", "Годлі 🔪", "Зірки ⭐"], "ask_bg": "Надішліть фон для позингу", "err_photo": "❌ Тільки фото!", "ask_mat": "4. Матеріал:", "ask_count": "5. Кількість (1-10):", "limit_err": "Ліміт 10 персонажів:", "done": "✅ Відправлено!" },
    "हिन्दी": { "ask_nick": "1. रोब्लॉक्स उपनाम:", "bad_nick": "❌ केवल अंग्रेजी अक्षर:", "ask_pay": "2. भुगतान:", "pay_list": ["रोबक्स 💸", "गॉडली 🔪", "सितारे ⭐"], "ask_bg": "पृष्ठभूमि भेजें", "err_photo": "❌ केवल चित्र!", "ask_mat": "4. सामग्री:", "ask_count": "5. संख्या (1-10):", "limit_err": "सीमा 10 है:", "done": "✅ भेज दिया!" },
    "Кыргызча": { "ask_nick": "1. Roblox ниги:", "bad_nick": "❌ Англисче гана:", "ask_pay": "2. Төлөм:", "pay_list": ["Робукс 💸", "Годли 🔪", "Жылдыз ⭐"], "ask_bg": "Фон жөнөтүңүз", "err_photo": "❌ Сүрөт гана!", "ask_mat": "4. Материал:", "ask_count": "5. Саны (1-10):", "limit_err": "Лимит 10 адам:", "done": "✅ Жиберилди!" },
    "Tiếng Việt": { "ask_nick": "1. Tên Roblox:", "bad_nick": "❌ Chỉ tiếng Anh:", "ask_pay": "2. Thanh toán:", "pay_list": ["Robux 💸", "Godly 🔪", "Sao ⭐"], "ask_bg": "Gửi ảnh nền", "err_photo": "❌ Chỉ nhận ảnh!", "ask_mat": "4. Chất liệu:", "ask_count": "5. Số lượng (1-10):", "limit_err": "Giới hạn 10:", "done": "✅ Đã gửi!" },
    "עברית": { "ask_nick": "1. כינוי רובלוקס:", "bad_nick": "❌ אנגלית בלבד:", "ask_pay": "2. תשלום:", "pay_list": ["רובאקס 💸", "גודלי 🔪", "כוכבים ⭐"], "ask_bg": "אנא שלח רקע", "err_photo": "❌ תמונות בלבד!", "ask_mat": "4. חומר:", "ask_count": "5. כמות (1-10):", "limit_err": "הגבלה של 10:", "done": "✅ נשלח!" },
    "Ελληνικά": { "ask_nick": "1. Όνομα Roblox:", "bad_nick": "❌ Μόνο αγγλικά:", "ask_pay": "2. Πληρωμή:", "pay_list": ["Robux 💸", "Godly 🔪", "Αστέρια ⭐"], "ask_bg": "Στείλτε φόντο", "err_photo": "❌ Μόνο φωτό!", "ask_mat": "4. Υλικό:", "ask_count": "5. Αριθμός (1-10):", "limit_err": "Όριο 10 άτομα:", "done": "✅ Στάλθηκε!" }
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
    if not re.match(r"^[A-Za-z0-9_]+$", message.text):
        msg = bot.send_message(message.chat.id, STRINGS[lang]["bad_nick"])
        bot.register_next_step_handler(msg, get_nick)
        return
    user_data[message.chat.id]["nick"] = message.text
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
    if message.content_type != 'photo':
        msg = bot.send_message(message.chat.id, STRINGS[lang]["err_photo"])
        bot.register_next_step_handler(msg, get_bg)
        return
    user_data[message.chat.id]["bg_id"] = message.photo[-1].file_id
    
    # Кнопки материала сразу после фото
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("PNG", "Обычный фон")
    msg = bot.send_message(message.chat.id, STRINGS[lang]["ask_mat"], reply_markup=markup)
    bot.register_next_step_handler(msg, get_mat)

def get_mat(message):
    lang = user_data[message.chat.id]["lang"]
    user_data[message.chat.id]["mat"] = message.text
    msg = bot.send_message(message.chat.id, STRINGS[lang]["ask_count"], reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, get_count)

def get_count(message):
    lang = user_data[message.chat.id]["lang"]
    if not message.text.isdigit():
        msg = bot.send_message(message.chat.id, "Введите число (1-10):")
        bot.register_next_step_handler(msg, get_count)
        return
    count = int(message.text)
    if count > 10:
        msg = bot.send_message(message.chat.id, STRINGS[lang]["limit_err"])
        bot.register_next_step_handler(msg, get_count)
        return
    
    d = user_data[message.chat.id]
    bot.send_message(message.chat.id, STRINGS[lang]["done"])
    
    # Анкета Ильфану
    report = (f"📑 **АНКЕТА ЗАКАЗА**\n\n👤 **Клиент:** @{message.from_user.username}\n"
              f"🌍 **Язык:** {d['lang']}\n🎮 **Ник:** `{d['nick']}`\n💰 **Оплата:** {d['pay']}\n"
              f"📦 **Материал:** {d['mat']}\n👥 **Кол-во:** {count}")
    bot.send_photo(ADMIN_ID, d["bg_id"], caption=report, parse_mode="Markdown")

bot.infinity_polling()
