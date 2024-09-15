import telebot
import yt_dlp
import requests
from TikTokApi import TikTokApi
from instagramy import InstagramPost
import speedtest
import ipaddress

# ضع توكن البوت الخاص بك هنا
API_TOKEN = '6265424443:AAEmHlTzANDravLJCb8BsVmiWzgZl0XFM3Y'

bot = telebot.TeleBot(API_TOKEN)

# رسالة الترحيب عند استخدام /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🎉 مرحباً! أنا بوت التحميل. يمكنني مساعدتك في تحميل محتويات يوتيوب، تيك توك، وانستاجرام. "
                          "إليك قائمة بالوظائف المتاحة:\n"
                          "1️⃣ أرسل رابط يوتيوب لتحميل الصوت أو الفيديو.\n"
                          "2️⃣ أرسل رابط تيك توك لتحميل الفيديو والوصف.\n"
                          "3️⃣ أرسل رابط انستاجرام لتحميل الصور/الفيديو والوصف.\n"
                          "4️⃣ استخدم الأمر /fast لقياس سرعة الإنترنت.\n"
                          "5️⃣ أرسل نطاق IP لتوليد قائمة عناوين IP كملف txt.")

# تحميل فيديو/صوت من يوتيوب
@bot.message_handler(func=lambda message: "youtube.com" in message.text or "youtu.be" in message.text)
def youtube_handler(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    btn1 = telebot.types.KeyboardButton('تحميل كصوت 🎵')
    btn2 = telebot.types.KeyboardButton('تحميل كفيديو 🎥')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "🎬 اختر نوع التحميل:", reply_markup=markup)

    bot.register_next_step_handler(message, lambda m: download_youtube(m, message.text))

def download_youtube(message, url):
    bot.send_message(message.chat.id, "⚡️")
    bot.send_message(message.chat.id, "📥 يتم تحميل المحتوى، يرجى الانتظار...")

    ydl_opts = {}
    if message.text == 'تحميل كصوت 🎵':
        ydl_opts = {'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]}
    elif message.text == 'تحميل كفيديو 🎥':
        ydl_opts = {'format': 'best'}
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info_dict)
            with open(file_name, 'rb') as f:
                bot.send_document(message.chat.id, f)
    except Exception as e:
        bot.send_message(message.chat.id, f"حدث خطأ أثناء التحميل: {e}")

# تحميل فيديو من تيك توك وإرسال الوصف
@bot.message_handler(func=lambda message: "tiktok.com" in message.text)
def tiktok_handler(message):
    bot.send_message(message.chat.id, "⚡️")
    bot.send_message(message.chat.id, "📥 يتم تحميل الفيديو، يرجى الانتظار...")
    
    try:
        api = TikTokApi()
        video = api.video(url=message.text)
        video_data = video.bytes()
        video_description = video.describe()
        
        bot.send_video(message.chat.id, video_data)
        bot.send_message(message.chat.id, f"📝 الوصف: {video_description}")
    except Exception as e:
        bot.send_message(message.chat.id, f"حدث خطأ أثناء التحميل: {e}")

# تحميل محتوى انستاجرام
@bot.message_handler(func=lambda message: "instagram.com" in message.text)
def instagram_handler(message):
    bot.send_message(message.chat.id, "⚡️")
    bot.send_message(message.chat.id, "📥 يتم تحميل المحتوى، يرجى الانتظار...")

    try:
        post = InstagramPost(message.text)
        media_type = post.media_type
        description = post.caption

        if media_type == 1:  # صورة
            bot.send_photo(message.chat.id, post.display_url)
        elif media_type == 2:  # فيديو
            bot.send_video(message.chat.id, post.video_url)
        
        bot.send_message(message.chat.id, f"📝 الوصف: {description}")
    except Exception as e:
        bot.send_message(message.chat.id, f"حدث خطأ أثناء التحميل: {e}")

# قياس سرعة الإنترنت
@bot.message_handler(commands=['fast'])
def speed_test(message):
    bot.send_message(message.chat.id, "⚡️")
    bot.send_message(message.chat.id, "🔄 يتم قياس سرعة الإنترنت، يرجى الانتظار...")
    
    try:
        st = speedtest.Speedtest()
        st.download()
        st.upload()
        results = st.results.dict()
        
        bot.send_message(message.chat.id, f"💡 سرعة التحميل: {results['download'] / 1_000_000:.2f} Mbps\n"
                                          f"💡 سرعة الرفع: {results['upload'] / 1_000_000:.2f} Mbps\n"
                                          f"📍 البينج: {results['ping']} ms")
    except Exception as e:
        bot.send_message(message.chat.id, f"حدث خطأ أثناء قياس السرعة: {e}")

# توليد قائمة IPs من نطاق
@bot.message_handler(func=lambda message: "/" in message.text)
def generate_ips(message):
    try:
        bot.send_message(message.chat.id, "⚡️")
        bot.send_message(message.chat.id, "🔄 يتم توليد قائمة IPs، يرجى الانتظار...")

        ip_net = ipaddress.ip_network(message.text.strip())
        ips = list(ip_net.hosts())
        
        with open("ips_list.txt", "w") as file:
            for ip in ips:
                file.write(str(ip) + "\n")

        with open("ips_list.txt", "rb") as file:
            bot.send_document(message.chat.id, file)
    except Exception as e:
        bot.send_message(message.chat.id, f"حدث خطأ أثناء توليد قائمة IPs: {e}")

# تشغيل البوت
bot.infinity_polling()