import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from yt_dlp import YoutubeDL

TOKEN = "8843002346:AAGoiw6I2NJHjegp-iwhaQ_9582tn07U2Hs"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Salom! Menga Instagram, TikTok yoki YouTube videosi silkasini yuboring, men uni yuklab beraman.")

@dp.message()
async def download_video(message: types.Message):
    url = message.text
    if not url.startswith("http"):
        await message.answer("Iltimos, faqat to'g'ri havola (silka) yuboring.")
        return

    msg = await message.answer("Video yuklanmoqda, iltimos kuting...")
    ydl_opts = {'outtmpl': 'video.%(ext)s', 'format': 'best'}

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        video_file = types.FSInputFile(filename)
        await message.reply_video(video=video_file, caption="Siz so'ragan video yuklab berildi!")
        os.remove(filename)
        await msg.delete()
    except Exception as e:
        await msg.edit_text("Xatolik yuz berdi. Silka noto'g'ri yoki ushbu videoni yuklab bo'lmadi.")
        if os.path.exists('video.mp4'): os.remove('video.mp4')

async def main():
    print("Bot muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
