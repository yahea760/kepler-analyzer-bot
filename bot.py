import telebot
import os

API_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """مرحبًا بك في غرفة المراقبة.

أنا Dr. Kepler… لست معالجك، ولا صديقك، بل الصوت الذي يدرّب وعيك على أن يرى ما لا يُقال.

هنا، لا نرد… بل نفكّر.
كل كلمة قيلت.
كل لحظة صمت.
كل إشارة مرّت أمامك وتجاهلتها.

مستعد تشوف اللي كان دايم قدامك؟

ابدأ الآن.
""")

@bot.message_handler(commands=['consult'])
def send_consult(message):
    bot.reply_to(message, "للاستشارات الخاصة، تواصل مع: @KeplerHimself")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, "اكتب /start لبدء التحليل، أو /consult للاستشارة.")

bot.infinity_polling()
