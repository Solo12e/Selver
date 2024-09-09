import telebot
from pytube import YouTube
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
        try:
            yt = YouTube(url)
            markup = telebot.types.InlineKeyboardMarkup()
            video_btn = telebot.types.InlineKeyboardButton('تحميل كفيديو 🎥', callback_data=f"video_{url}")
            audio_btn = telebot.types.InlineKeyboardButton('تحميل كصوت 🎧', callback_data=f"audio_{url}")
            markup.add(video_btn, audio_btn)
            bot.reply_to(message, f"اختر نوع التحميل لـ {yt.title}:", reply_markup=markup)
        except Exception as e:
            bot.reply_to(message, f"الرابط غير صالح أو حدث خطأ أثناء التحميل: {str(e)}")
    else:
        bot.reply_to(message, "الرجاء إرسال رابط يوتيوب صالح.")

# التعامل مع ضغطات الأزرار
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    url = call.data.split('_')[1]
    action = call.data.split('_')[0]
    
    try:
        yt = YouTube(url)
        if action == "video":
            bot.send_message(call.message.chat.id, "⌛️ جاري تحميل الفيديو...")
            video_stream = yt.streams.get_highest_resolution()
            video_path = video_stream.download()
            if os.path.exists(video_path):
                with open(video_path, 'rb') as video:
                    bot.send_video(call.message.chat.id, video)
                os.remove(video_path)
            else:
                bot.send_message(call.message.chat.id, "فشل تحميل الفيديو.")
        elif action == "audio":
            bot.send_message(call.message.chat.id, "⌛️ جاري تحميل الصوت...")
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_path = audio_stream.download()
            new_file = audio_path.replace(".mp4", ".mp3")
            os.rename(audio_path, new_file)
            if os.path.exists(new_file):
                with open(new_file, 'rb') as audio:
                    bot.send_audio(call.message.chat.id, audio)
                os.remove(new_file)
            else:
                bot.send_message(call.message.chat.id, "فشل تحميل الصوت.")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"حدث خطأ أثناء التحميل: {str(e)}")

# بدء البوت
bot.polling()