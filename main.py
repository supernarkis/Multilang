import configparser
from telethon import TelegramClient, events
import workers

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("config.ini")  # читаем конфиг

tg_user_id = config["tg_user"]["tg_user_id"]
api_id = config["tg_user"]["api_id"]
api_hash = config["tg_user"]["api_hash"]
phone = config["tg_user"]["phone"]

# Создаем клиента Telegram
client = TelegramClient('anon', api_id, api_hash)

@client.on(events.NewMessage(pattern='^/start$'))
async def start(event):
    await event.respond('Привет, отправь мне ссылку на видео.')

@client.on(events.NewMessage)
async def text_handler(event):
    if event.is_private and event.text and 'youtu' in event.text:
        video_url = event.text.replace('youtube.com/shorts/', 'youtube.com/watch?v=').replace('youtu.be/', 'youtube.com/watch?v=').replace('?si', '&').split('&')[0]

        await workers.process_video(client, event, video_url)

if __name__ == '__main__':
    client.start()
    print("Бот запущен.")
    client.run_until_disconnected()
