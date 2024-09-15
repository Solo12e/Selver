import speedtest as st
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# أدخل توكن البوت الخاص بك هنا
TOKEN = '6265424443:AAEmHlTzANDravLJCb8BsVmiWzgZl0XFM3Y'

# اسم المستخدم الخاص بك
USERNAME = "@MB_758"

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f"مرحبًا! أنا بوت فحص سرعة الإنترنت. أرسل /speedtest لبدء الفحص.\n\nMade by: {USERNAME}")

def speedtest_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f"⚡️ جاري فحص سرعة الإنترنت، يرجى الانتظار...\n\nMade by: {USERNAME}")

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
        update.message.reply_text(response)
    except AttributeError:
        update.message.reply_text(f"❌ حدث خطأ في فحص السرعة. تأكد من أن مكتبة speedtest-cli مثبتة بشكل صحيح.\n\nMade by: {USERNAME}")

def main() -> None:
    # إنشاء Updater وربطه بالتوكن
    updater = Updater(TOKEN)

    # الحصول على Dispatcher لإضافة مكونات البوت
    dispatcher = updater.dispatcher

    # ربط الأوامر بالدوال المناسبة
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("speedtest", speedtest_command))

    # بدء تشغيل البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
