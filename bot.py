import telebot
import os

API_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

# تخزين الحالة لكل مستخدم
user_state = {}
user_data = {}
consult_requests = {}

# رقم معرفك في تيليجرام
admin_id = 1354595286

# الأسئلة التفاعلية لتمرين 3x3
questions = [
    "اكتب الموقف اللي مرّ عليك أو شفته اليوم وغير تركيزك.",
    "وش الشعور أو الأفكار اللي راودتك أو حسّيت فيها خلال هذا الموقف؟",
    "وش الشي اللي لمسك وأثر فيك من هذا الموقف؟"
]

@bot.message_handler(commands=['start'])
def start_message(message):
    uid = message.from_user.id
    user_state[uid] = 0
    user_data[uid] = []
    bot.reply_to(message,
        "معاك Dr. Kepler، مرحبًا بك في غرفة المراقبة.\n"
        "أنا … لست معالجك، ولا صديقك، بل الصوت الذي يدرّب وعيك على أن يرى ما لا يُقال.\n\n"
        + questions[0])

@bot.message_handler(commands=['clear'])
def clear_notes(message):
    uid = message.from_user.id
    user_state[uid] = 0
    user_data[uid] = []
    bot.reply_to(message, "تم حذف مذكرتك بالكامل. ابدأ من جديد.\n\n" + questions[0])

@bot.message_handler(commands=['contact'])
def contact_info(message):
    bot.reply_to(message, "للتواصل المباشر مع Dr. Kepler: @KeplerHimself")

@bot.message_handler(func=lambda m: m.text.lower() == "استشارة")
def start_consult(message):
    uid = message.from_user.id
    consult_requests[uid] = "awaiting_question"
    bot.reply_to(message, "ما سؤالك؟ اكتبه الآن وسأرسله لـ Dr. Kepler مباشرة.")

@bot.message_handler(func=lambda m: m.from_user.id in consult_requests and consult_requests[m.from_user.id] == "awaiting_question")
def receive_consult_question(message):
    uid = message.from_user.id
    question = message.text
    consult_requests[uid] = question
    bot.reply_to(message, "تم استلام سؤالك، سيتم الرد عليك قريبًا.")
    bot.send_message(admin_id, f"[استشارة جديدة]\nمن المستخدم: {uid}\n\n{question}")

@bot.message_handler(func=lambda m: m.text.lower().startswith("رد على") and m.from_user.id == admin_id)
def admin_reply(message):
    try:
        parts = message.text.split(":", 1)
        id_part = parts[0].strip()
        reply_part = parts[1].strip()
        uid = int(id_part.replace("رد على", "").strip())
        bot.send_message(uid, f"رد Dr. Kepler على استشارتك:\n\n{reply_part}")
        bot.reply_to(message, f"تم إرسال ردك للمستخدم {uid}.")
    except:
        bot.reply_to(message, "صيغة خاطئة. اكتب:\nرد على [ID]: (نص الرد)")

@bot.message_handler(func=lambda m: True)
def handle_input(message):
    uid = message.from_user.id

    if uid in consult_requests and consult_requests[uid] == "awaiting_question":
        return  # تجنّب تكرار السؤال إذا أرسل بدون أمر

    if uid not in user_state:
        user_state[uid] = 0
        user_data[uid] = []
        bot.reply_to(message, questions[0])
        return

    state = user_state[uid]
    user_data[uid].append(message.text)

    if state < 2:
        user_state[uid] += 1
        bot.reply_to(message, questions[state + 1])
    else:
        entry = user_data[uid]
        result = (
            "تحليلك الكامل:\n\n"
            f"1. الموقف: {entry[0]}\n"
            f"2. الشعور/الأفكار: {entry[1]}\n"
            f"3. التأثير: {entry[2]}\n\n"
            "اكتب /clear لإعادة التمرين، أو استمر لتكرار التجربة."
        )
        bot.reply_to(message, result)
        user_state[uid] = 0
        user_data[uid] = []
        bot.send_message(uid, questions[0])

bot.infinity_polling()
