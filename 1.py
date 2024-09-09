import telebot
import yt_dlp
import os

# توكن البوت
TOKEN = "6265424443:AAEmHlTzANDravLJCb8BsVmiWzgZl0XFM3Y"
bot = telebot.TeleBot(TOKEN)

# رسالة ترحيب أو تعليمات
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "أرسل رابط اليوتيوب ، Made by @MB_758 .")

# استلام رابط اليوتيوب من المستخدم
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "youtube.com" in url or "youtu.be" in url:
        markup = telebot.types.InlineKeyboardMarkup()
        video_btn = telebot.types.InlineKeyboardButton('تحميل كفيديو 🎥', callback_data=f"video_{url}")
        audio_btn = telebot.types.InlineKeyboardButton('تحميل كصوت 🎧', callback_data=f"audio_{url}")
        markup.add(video_btn, audio_btn)
        bot.reply_to(message, "اختر نوع التحميل:", reply_markup=markup)
    else:
        bot.reply_to(message, "الرجاء إرسال رابط يوتيوب صالح.")

# التعامل مع ضغطات الأزرار
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    url = call.data.split('_')[1]
    action = call.data.split('_')[0]
    
    ydl_opts = {}
    
    if action == "video":
        bot.send_message(call.message.chat.id, "⌛️ جاري تحميل الفيديو...")
        ydl_opts = {
            'format': 'bestvideo+bestaudio',
            'outtmpl': 'video.%(ext)s'
        }
    elif action == "audio":
        bot.send_message(call.message.chat.id, "⌛️ جاري تحميل الصوت...")
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': 'audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.download([url])
            if action == "video":
                video_path = "video.mp4"
                if os.path.exists(video_path):
                    with open(video_path, 'rb') as video:
                        bot.send_video(call.message.chat.id, video)
                    os.remove(video_path)
                else:
                    bot.send_message(call.message.chat.id, "فشل تحميل الفيديو.")
            elif action == "audio":
                audio_path = "audio.mp3"
                if os.path.exists(audio_path):
                    with open(audio_path, 'rb') as audio:
                        bot.send_audio(call.message.chat.id, audio)
                    os.remove(audio_path)
                else:
                    bot.send_message(call.message.chat.id, "فشل تحميل الصوت.")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"حدث خطأ أثناء التحميل: {str(e)}")

# بدء البوت
bot.polling()
