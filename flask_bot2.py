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


menu = [{'name': 'Главная', 'url': '/'},
        {'name': 'О нас', 'url': 'about'},
        {'name': 'FAQ', 'url': 'faq'},
        {'name': 'Донаты', 'url': 'donates'},
        {'name': 'Рассылка', 'url': 'feedback'}]


TOKEN = 'token

bot = telebot.TeleBot(TOKEN, parse_mode='MarkDown')


def run_bot():
    bot.infinity_polling()


bot_thread = threading.Thread(target=run_bot)


@app.route('/')
def index():
    return render_template('index.html', menu=menu)


@app.route('/about')
def about():
    return render_template('about.html', menu=menu)


@app.route('/faq')
def faq():
    return render_template('faq.html', menu=menu)


@app.route('/donates')
def donates():
    return render_template('donates.html', menu=menu)


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
    return render_template('feedback.html', title='Рассылка', menu=menu)


@app.route("/start-bot")
def start_bot():
    return render_template('start_bot.html', title='Бот', menu=menu)


if __name__ == "__main__":
    app.run(debug=True)
