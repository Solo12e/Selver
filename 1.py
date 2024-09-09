import telebot
import yt_dlp
import os
import subprocess

# توكن البوت
TOKEN = "6265424443:AAEmHlTzANDravLJCb8BsVmiWzgZl0XFM3Y"
bot = telebot.TeleBot(TOKEN)

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 ميغابايت

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
            ydl.download([url])
            
            if action == "video":
                video_path = "video.mp4"
                if os.path.exists(video_path):
                    if os.path.getsize(video_path) <= MAX_FILE_SIZE:
                        # إذا كان الفيديو أقل من 50 ميغابايت، قم بإرساله مباشرة
                        with open(video_path, 'rb') as video:
                            bot.send_video(call.message.chat.id, video)
                    else:
                        # تقسيم الفيديو إلى أجزاء صغيرة وإرسالها
                        split_and_send_file(video_path, call.message.chat.id)
                    os.remove(video_path)
            elif action == "audio":
                audio_path = "audio.mp3"
                if os.path.exists(audio_path):
                    if os.path.getsize(audio_path) <= MAX_FILE_SIZE:
                        # إذا كان الصوت أقل من 50 ميغابايت، قم بإرساله مباشرة
                        with open(audio_path, 'rb') as audio:
                            bot.send_audio(call.message.chat.id, audio)
                    else:
                        # تقسيم الصوت إلى أجزاء صغيرة وإرسالها
                        split_and_send_file(audio_path, call.message.chat.id)
                    os.remove(audio_path)
    except Exception as e:
        bot.send_message(call.message.chat.id, f"حدث خطأ أثناء التحميل أو الإرسال: {str(e)}")

def split_and_send_file(file_path, chat_id):
    try:
        # تحديد اسم الملف والامتداد
        file_name, file_extension = os.path.splitext(file_path)
        output_pattern = f"{file_name}_part_%03d{file_extension}"
        
        # تقسيم الملف باستخدام ffmpeg
        command = [
            'ffmpeg', '-i', file_path, '-c', 'copy', '-map', '0',
            '-f', 'segment', '-segment_time', '00:01:00', output_pattern
        ]
        subprocess.run(command, check=True)
        
        # إرسال الأجزاء المقطعة للمستخدم
        part_number = 0
        while True:
            part_file = output_pattern % part_number
            if os.path.exists(part_file):
                with open(part_file, 'rb') as part:
                    bot.send_document(chat_id, part)
                os.remove(part_file)
                part_number += 1
            else:
                break
    except Exception as e:
        bot.send_message(chat_id, f"حدث خطأ أثناء تقسيم وإرسال الملف: {str(e)}")

# بدء البوت
bot.polling()
