# Multilang
Небольшой бот, которым может переводить youtube видео с английскогоб немецкого, французского и др. на русский. 

Ограничения:
- видео длительностью более 4 часов не будут переведены
- некторые языки могут переводиться не полностью или вообще не переводиться.
- 

## install
  1. Установите NodeJS 18+
  2. Установите vot-cli глобально:
```
npm install -g vot-cli
```
подробнее тут https://github.com/FOSWLY/vot-cli

  3.Установите ffmpeg:
```
sudo apt update
sudo apt ugrade
sudo apt install ffmpeg
```
  4. Установите yt-dlp:
```
sudo apt install yt-dlp
```
5. Склонируйте репозиторий в выбранную папку перейдите в нее и настройте виртуальное окружение
   (предполагается что у вас установлен питон 3.6+ и venv):
```
git clone https://github.com/supernarkis/Multilang.git
cd ./Multilang
python -m venv myvenv
source myvenv/bin/activate
pip install -r require.txt
```
7. В файле example-config.ini токен бота, id и хеш клиентского приложения и сохраните как config.ini 
8. Запустите бота:
```
python main.py
```


