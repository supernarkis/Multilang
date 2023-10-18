import subprocess
import sys
import shutil
import os
import threading
import telebot
from telethon import TelegramClient
import asyncio


api_id = 26857008
api_hash = 'ad41412989b57a0f91b97ae6195bc7b0'
phone = '+77054399634'
client = TelegramClient('anon', api_id, api_hash)

token = '6356979499:AAHIdNwHe9yANc0bRfrqIS_xAml1HqZVGAY'
bot = telebot.TeleBot(token)


def process_video( message ):
    video_link = message.text
    temp_dir = f'./temp/{message.message_id}'
    temp_video_dir = f"{temp_dir}/video"
    temp_video = f"{temp_video_dir}/%(title)s.%(ext)s"
    temp_audio = f"{temp_dir}/audio"
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(temp_video_dir, exist_ok=True)
    os.makedirs(temp_audio, exist_ok=True)

    yd = subprocess.Popen(["yt-dlp", "-o", temp_video, video_link,"--format", "22"], shell=True, stdout=sys.stdout)
    yd.communicate()

    votcmd = ["powershell.exe", " vot-cli " + video_link + f" --output={temp_audio}"]
    vot = subprocess.Popen(votcmd, shell=True, stdout=sys.stdout.reconfigure(encoding='utf-8'))
    vot.communicate()

    temp_video_file_name = os.listdir(temp_video_dir)[0]
    temp_video_file = temp_video_dir + "/" + temp_video_file_name
    temp_audio_file = temp_audio + "/" + os.listdir(temp_audio)[0]

    cmd = 'ffmpeg -i \"' + temp_video_file + '\"' \
                ' -i \"' + temp_audio_file + '\" ' \
                '-c:v copy -b:a 128k ' \
                '-filter_complex \"[0:a] volume=0.12 [original]; [original][1:a] amix=inputs=2:duration=longest [audio_out]\" ' \
                '-map 0:v ' \
                '-map \"[audio_out]\" ' \
                '-y \"' + temp_video_file_name + '\"'

    ff = subprocess.Popen(["powershell.exe", cmd], shell=True, stdout=sys.stdout.reconfigure(encoding='utf-8'))
    ff.communicate()

    shutil.rmtree(temp_dir)
    return (temp_video_file_name)


@bot.message_handler(commands=['start'])
def start( message ):
    bot.send_message(message.chat.id, f'i see you')


@bot.message_handler(content_types=['text'])
def text_handler( message ):
    #если с ютуба
    if "tube" in message.text:
        threading.Thread(target=video_translator, args=(bot, message)).start()


def video_translator( bot, message ):
        # заказать перевод и переслать заказчику
        filename = process_video(message)
        send_file(filename, message.from_user.id)


@bot.message_handler(content_types=['document', 'video'])
def file_handler( message ):
    # Файлы от админа с caption
    if message.from_user.id == 5904707497 and message.caption:
        # Создаем новый поток для пересылки
        threading.Thread(target=redirect_to_customer, args=(bot, message)).start()


def redirect_to_customer(bot, message ):
    #Пересылаем файл по id укзанному в caption
    try:
        bot.send_video(message.caption, str(message.document.file_id))
    except:
        print("Не удалось отправить файл ", message.document.file_name, " в чат c id ", message.caption)


def send_file( filename, id ):
    try:
        if os.path.getsize(f"./{filename}") <= 49*1024*1024:
            with open(f'./{filename}', "rb") as file:
                bot.send_video(id, file)
        else:

            async def tasker (filename, id):
                task = asyncio.create_task(send_file_fromclient(filename, id))
                await task

            client.connect()
            asyncio.run(tasker(filename, id))

    except():
        print("Error occurred on function main.py - send_file")
    finally:
        os.remove(f"./{filename}")
    return


async def send_file_fromclient( filename, id ):
    await client.send_file('Multilang_bot', f"./{filename}", caption=str(id))



print("Run!")
bot.polling()

