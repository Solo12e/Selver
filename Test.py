import speedtest as st
import telebot

# أدخل توكن البوت الخاص بك هنا
TOKEN = '6265424443:AAEmHlTzANDravLJCb8BsVmiWzgZl0XFM3Y'

# اسم المستخدم الخاص بك
USERNAME = "@MB_758"

# إنشاء كائن البوت
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, f"مرحبًا! أنا بوت فحص سرعة الإنترنت. أرسل /speedtest لبدء الفحص.\n\nMade by: {USERNAME}")

@bot.message_handler(commands=['speedtest'])
def speedtest_command(message):
    bot.reply_to(message, f"⚡️ جاري فحص سرعة الإنترنت، يرجى الانتظار...\n\nMade by: {USERNAME}")

    # محاولة استخدام الكائن Speedtest
    try:
        speed_test = st.Speedtest()
        download_speed = speed_test.download() / 10**6  # تحويل إلى ميغابت
        upload_speed = speed_test.upload() / 10**6  # تحويل إلى ميغابت
        ping = speed_test.results.ping

        # إنشاء الرد بالإيموجيات
        response = (
            f"نتائج فحص سرعة الإنترنت:\n\n"
            f"📥 سرعة التحميل: {download_speed:.2f} Mbps\n"
            f"📤 سرعة الرفع: {upload_speed:.2f} Mbps\n"
            f"📶 زمن الاستجابة (Ping): {ping} ms\n\n"
            f"Made by: {USERNAME}"
        )
        bot.reply_to(message, response)
    except AttributeError:
        bot.reply_to(message, f"❌ حدث خطأ في فحص السرعة. تأكد من أن مكتبة speedtest-cli مثبتة بشكل صحيح.\n\nMade by: {USERNAME}")

# بدء البوت
bot.polling()
