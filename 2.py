import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import yt_dlp
import os

API_TOKEN = '6265424443:AAEmHlTzANDravLJCb8BsVmiWzgZl0XFM3Y'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def search_youtube_video(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        if 'entries' in info:
            return info['entries'][0]['url']
        else:
            return None

def download_youtube_video_as_mp3(url):
    output_filename = 'n7.mp3'
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'n7.%(ext)s',  # Ensure the output file is named correctly
        'postprocessor_args': [
            '-ar', '16000',
            '-ac', '1'
        ],
        'keepvideo': False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    # Rename file to expected name if necessary
    if os.path.exists('n7.mp3'):
        os.rename('n7.mp3', output_filename)
    
    return output_filename

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("أرسل لي اسم الفيديو من YouTube لتحويله إلى MP3!")

@dp.message_handler()
async def handle_message(message: types.Message):
    query = message.text

    if query:
        await message.reply("جاري البحث عن الفيديو وتحميله...")

        # Add a small delay to avoid rapid requests
        await asyncio.sleep(5)

        try:
            video_url = search_youtube_video(query)

            if video_url:
                mp3_file = download_youtube_video_as_mp3(video_url)

                if os.path.exists(mp3_file):
                    with open(mp3_file, 'rb') as audio:
                        # Send the audio file to the user
                        await message.reply_document(audio)

                    # Remove the file after sending
                    os.remove(mp3_file)
                else:
                    await message.reply("فشل تحميل الملف.")
            else:
                await message.reply("لم يتم العثور على الفيديو.")

        except Exception as e:
            await message.reply(f"حدث خطأ: {str(e)}")
    else:
        await message.reply("يرجى إرسال اسم الفيديو.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
