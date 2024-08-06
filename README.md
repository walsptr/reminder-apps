# Simple Apps reminder to bot telegram

Pada file app.py, edit baris parameter
```
TELEGRAM_BOT_TOKEN = isi dengan bot token telegram yang digunakan
STATIC_CHAT_ID = isi dengan chat id/channel id telegram yang digunakan
```

## Running on prem
```
apt install python3 python3-venv

//clone source code
git clone https://github.com/walsptr/reminder-apps.git
cd reminder-apps

//running virtual env python
python3 -m venv .
. bin/activate

//install dependencise
pip install -r requirements.txt

//running script
python3 app.py
```

## Running on Docker
Untuk running didocker jalankan perintah dibawah
```
docker build -t reminder-apps .
docker run -d --name reminder-apps -p 5000:5000 reminder-apps
```


