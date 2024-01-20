from flask import Flask, render_template, request, redirect, url_for, g
import threading
import telebot
import sqlite3 as sq
import os


DATABASE = 'message_ids.db'
DEBUG = True
SECRET_KEY = 'fdgdfgdfggf786hfg6hfg6h7f'

app = Flask(__name__)
app.config.from_object(__name__)


app.config.update(dict(DATABASE=os.path.join(app.root_path, 'message_ids.db')))


def connect_db():
    conn = sq.connect(app.config['DATABASE'])
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


def fetch_chat_ids(db):
    cursor = db.cursor()
    cursor.execute('SELECT chat_id FROM chat_ids')
    res = cursor.fetchall()
    lst = []
    for i in res:
        lst.append(i[0])
    return lst


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


TOKEN = '6372785791:AAGPWCjzc8cSiARhuMBUwsbVumjuf-uPCj0'

bot = telebot.TeleBot(TOKEN, parse_mode='MarkDown')


def run_bot():
    bot.infinity_polling()


bot_thread = threading.Thread(target=run_bot)


@app.route('/feedback', methods=['POST', 'GET'])
def feedback():
    db = get_db()

    if request.method == 'POST':
        bot_thread.start()
        chat_ids = fetch_chat_ids(db)
        message = request.form['message']
        for i in chat_ids:
            bot.send_message(i, message)
        return redirect(url_for('start_bot'))
    return render_template('feedback.html')


@app.route("/start-bot")
def start_bot():
    return 'Сообщение отправлено'


if __name__ == "__main__":
    app.run(debug=True)
