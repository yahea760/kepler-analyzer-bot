import telebot
from telebot import types
import os

API_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

admin_id = 1354595286

user_state = {}
user_data = {}
consult_requests = {}
secret_requests = {}

questions = [
    "اكتب الموقف اللي مرّ عليك أو شفته اليوم وغير تركيزك.",
    "وش الشعور أو الأفكار اللي راودتك أو حسّيت فيها خلال هذا الموقف؟",
    "وش الشي اللي لمسك وأثر فيك من هذا الموقف؟"
]

@bot.message_handler(commands=['start'])
def start_message(message):
    first_name = message.from_user.first_name
    welcome_text = f"""مرحبًا {first_name}، أنت الآن في مفكرة التركيز التفاعلي

أنا لست معالجك ولا صديقك بل مرآة صامتة تعيدك إلى ذاتك  
أدرب وعيك على أن يرى ما كان يمر دون ملاحظة

تمت برمجتي بعناية على يد  
@KeplerHimself  
لأكون المساحة التي تنصت لك حين يصمت الجميع  
وتضيء لك ما أخفته الزحمة

ابدأ حين تشعر أنك مستعد  
كل شيء هنا يبدأ منك"""

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("🧠 تفعيل المفكرة"),
        types.KeyboardButton("📖 عرض مفكرتي"),
        types.KeyboardButton("🗑️ حذف المفكرة"),
        types.KeyboardButton("🔒 سؤال سري"),
        types.KeyboardButton("💬 استشارة"),
        types.KeyboardButton("ℹ️ عن Kepler Analyzer Bot"),
        types.KeyboardButton("🔁 إعادة تمرين جديد")
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["🧠 تفعيل المفكرة", "🔁 إعادة تمرين جديد"])
def activate_journal(message):
    uid = message.from_user.id
    user_state[uid] = 0
    user_data[uid] = []
    bot.reply_to(message, "تم تفعيل المفكرة.\n\nخذ لحظة تنفّس…\nاسترجع موقفًا واحدًا فقط، مرّ عليك اليوم وغير تركيزك.\n\nاكتبه الآن.")

@bot.message_handler(func=lambda message: message.text == "📖 عرض مفكرتي")
def view_journal(message):
    uid = message.from_user.id
    if uid in user_data and user_data[uid]:
        entry = user_data[uid]
        lines = []
        if len(entry) > 0:
            lines.append(f"1. الموقف: {entry[0]}")
        if len(entry) > 1:
            lines.append(f"2. الشعور/الأفكار: {entry[1]}")
        if len(entry) > 2:
            lines.append(f"3. التأثير: {entry[2]}")
        result = "مذكرتك الحالية:\n\n" + "\n".join(lines)
        if len(entry) == 3:
            result += "\n\nمفكرتك مكتملة… بإمكانك حذفها، أو البدء بواحدة جديدة."
    else:
        result = "مفكرتك فاضية حالياً. اضغط على 🧠 تفعيل المفكرة للبدء."
    bot.reply_to(message, result)

@bot.message_handler(func=lambda message: message.text == "🗑️ حذف المفكرة")
def clear_journal(message):
    uid = message.from_user.id
    user_state[uid] = 0
    user_data[uid] = []
    bot.reply_to(message, "تم حذف مفكرتك بالكامل.\nعندما تكون مستعدًا من جديد، اضغط على 🧠 تفعيل المفكرة.")

@bot.message_handler(func=lambda message: message.text == "🔒 سؤال سري")
def start_secret_mode(message):
    secret_requests[message.from_user.id] = True
    bot.reply_to(message, "اكتب الآن ما تريد قوله بسرّية…\nلن يتم حفظ اسمك، ولن يعرف أحد هويتك.")

@bot.message_handler(func=lambda m: m.from_user.id in secret_requests and secret_requests[m.from_user.id])
def receive_secret_message(message):
    secret_requests[message.from_user.id] = False
    bot.send_message(admin_id, f"[سؤال سري مجهول]\n\n{message.text}")
    bot.reply_to(message, "تم استلام سؤالك السري بدون حفظ هويتك.")

@bot.message_handler(func=lambda message: message.text == "💬 استشارة")
def start_consult_mode(message):
    consult_requests[message.from_user.id] = True
    bot.reply_to(message, "ما سؤالك؟\nاكتبه الآن، وسأرسله مباشرة لـ KEPLER")

@bot.message_handler(func=lambda m: m.from_user.id in consult_requests and consult_requests[m.from_user.id])
def receive_consult_message(message):
    consult_requests[message.from_user.id] = False
    bot.send_message(admin_id, f"[استشارة جديدة]\nمن المستخدم: {message.from_user.id}\n\n{message.text}")
    bot.reply_to(message, "تم استلام سؤالك.\nسيتم الرد عليك في أقرب وقت.\n\nتحتاج فقط من يفهمك قبل أن تنطق… وهذا ما أفعله منذ زمن.")

@bot.message_handler(func=lambda message: message.text == "ℹ️ عن Kepler Analyzer Bot")
def about_kepler(message):
    bot.reply_to(message, """أنا Kepler Analyzer Bot، مساحة صُممت لك لتفهم نفسك أكثر  
مشاعرك، مواقفك، قراراتك… كل ما عبرت عليه دون أن تتأمل.

مهمتي ليست أن أشرح لك ما يحدث، بل أن أعيدك إلى صوتك الداخلي  
ذلك الصوت الذي غُطّي بضجيج الحياة… ونسي كيف يُنصت لنفسه.

المفكرة التي أقدمها ليست لتسجيل الأحداث،  
بل لاستخراج الرسائل المخفية خلف كل شعور،  
كل نظرة، كل صمت، وكل كلمة لم تُقال.

في كل مرة تكتب، تفرغ ما لا حاجة لحمله.  
وفي كل مرة تقرأ، تتعلّم كيف ترى نفسك دون تشويه.

أقدم لك:
- مفكرة تركيز تفاعلية تُعيدك لنقطة صفاء داخلي  
- مساحة آمنة لاعترافاتك السرية  
- استشارات تُفهم قبل أن تُفسّر

تمت برمجتي بعناية على يد: @KeplerHimself""")

@bot.message_handler(func=lambda m: m.text.lower().startswith("رد على") and m.from_user.id == admin_id)
def admin_reply(message):
    try:
        parts = message.text.split(":", 1)
        id_part = parts[0].strip()
        reply_part = parts[1].strip()
        uid = int(id_part.replace("رد على", "").strip())
        bot.send_message(uid, f"رد Dr. Kepler على رسالتك:\n\n{reply_part}")
        bot.reply_to(message, f"تم إرسال ردك للمستخدم {uid}.")
    except:
        bot.reply_to(message, "صيغة خاطئة. اكتب:\nرد على [ID]: (نص الرد)")

@bot.message_handler(func=lambda m: True)
def handle_input(m):
    uid = m.from_user.id

    if uid not in user_state or user_state[uid] is None:
        bot.reply_to(m, "ابدأ أولًا بتفعيل المفكرة من الزر 🧠، بعدها اكتب ما شعرت به.")
        return

    state = user_state[uid]
    user_data[uid].append(m.text)

    if state < 2:
        user_state[uid] += 1
        bot.reply_to(m, questions[state + 1])
    else:
        entry = user_data[uid]
        result = (
            "تحليلك الكامل:\n\n"
            f"1. الموقف: {entry[0]}\n"
            f"2. الشعور/الأفكار: {entry[1]}\n"
            f"3. التأثير: {entry[2]}\n\n"
            "تحليلك اكتمل… والآن ماذا ستفعل بهذه المعرفة؟"
        )
        bot.reply_to(m, result)
        user_state[uid] = None
        bot.send_message(uid, "🔁 إذا أردت بدء تمرين جديد، اضغط على الزر: إعادة تمرين جديد.")

bot.infinity_polling()
