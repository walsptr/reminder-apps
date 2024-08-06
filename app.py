from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import threading
import time
import requests

app = Flask(__name__)
DATABASE = 'reminders.db'
TELEGRAM_BOT_TOKEN = '7463164282:AAFteqjK6PTOdyYln-FNUNtFMnW9PVobC2A'
STATIC_CHAT_ID = '-1002165408003'  # Ganti dengan chat ID statis Anda
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reminders
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, message TEXT, remind_datetime TEXT)''')
    conn.commit()
    conn.close()

def add_reminder(username, message, remind_date, remind_time):
    remind_datetime = f"{remind_date} {remind_time}"
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO reminders (username, message, remind_datetime) VALUES (?, ?, ?)",
              (username, message, remind_datetime))
    conn.commit()
    conn.close()

def send_message_to_telegram(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def check_reminders():
    while True:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT id, username, message, remind_datetime FROM reminders WHERE remind_datetime <= ?",
                  (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))
        rows = c.fetchall()
        for row in rows:
            text = f"@{row[1]}\n{row[2]}"
            send_message_to_telegram(STATIC_CHAT_ID, text)
            c.execute("DELETE FROM reminders WHERE id = ?", (row[0],))
        conn.commit()
        conn.close()
        time.sleep(60)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        message = request.form.get('message')
        remind_date = request.form.get('remind_date')
        remind_time = request.form.get('remind_time')
        if not username or not message or not remind_date or not remind_time:
            return "All fields are required."
        add_reminder(username, message, remind_date, remind_time)
        return redirect(url_for('index'))
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    threading.Thread(target=check_reminders, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=True)

