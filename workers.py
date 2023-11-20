import asyncio
import os
import shutil
import subprocess
import sys


async def process_video(client, event, video_url):
    temp_dir = f'temp/{event.id}'
    print(event.id)
    temp_video_dir = f'{temp_dir}/video'
    temp_audio_dir = f'{temp_dir}/audio'
    video_file = f"{temp_video_dir}/%(title)s.%(ext)s"

    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(temp_video_dir, exist_ok=True)
    os.makedirs(temp_audio_dir, exist_ok=True)

    await download_video(event, video_url, video_file)
    await download_audio(event, video_url, temp_audio_dir)
    video_file = f'{temp_video_dir}/{os.listdir(temp_video_dir)[0]}'
    audio_file = f'{temp_audio_dir}/{os.listdir(temp_audio_dir)[0]}'
    result_file = f'{temp_dir}/{os.listdir(temp_video_dir)[0]}'
    try:
        if video_file and audio_file:
            await edit_video(video_file, audio_file, result_file)
            if result_file:
                await send_large_file(client, event, result_file)
    finally:
        shutil.rmtree(temp_dir)

async def download_video(event, video_url, video_file):
    try:
        process = await asyncio.create_subprocess_exec('yt-dlp', video_url, '-o', video_file, "-f", "22")
        await process.wait()
    except Exception as e:
        await event.respond(f'Не удалось получить видео по ссылке: {str(e)}')
        print(f'Ошибка в download_video: {str(e)}')

async def download_audio(event, video_url, temp_audio_dir):
    try:
        process = subprocess.Popen(['vot-cli', f'--output={temp_audio_dir}', video_url], shell=True, stdout=sys.stdout.reconfigure(encoding='utf-8'))
        process.communicate()
        process.wait()
        print('Переведенный аудио файл скачан')
    except Exception as e:
        await event.respond(f'Не удалось получить перевод: {str(e)}')
        print(f'Ошибка при скачивании переведенного аудио: {str(e)}')

async def edit_video(video_file, audio_file, result_file):
    try:
        process = await asyncio.create_subprocess_exec(
            'ffmpeg',
            '-i', video_file,
            '-i', audio_file,
            '-c:v', 'copy',
            '-b:a', '128k',
            '-filter_complex', '[0:a] volume=0.12 [original]; [original][1:a] amix=inputs=2:duration=longest [audio_out]',
            '-map', '0:v',
            '-map', '[audio_out]',
            '-y', result_file
        )
        await process.wait()
        print('Видео собрано')
    except Exception as e:
        print(f'Ошибка при пересборке видео: {str(e)}')

async def send_large_file(client, event, file_path):
    try:
        await client.send_file(event.chat_id, os.path.abspath(file_path), mime_type='video/mp4')
    except Exception as e:
        await event.respond(f'Не узалось загрузить переведенное видео в телеграм: {str(e)}')
        print(f'Произошла ошибка в send_large_file: {str(e)}')


if __name__ == '__main__':
    client.start()
    client.run_until_disconnected()
