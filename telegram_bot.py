import telebot
import sqlite3 as sq


TOKEN = '6372785791:AAGPWCjzc8cSiARhuMBUwsbVumjuf-uPCj0'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'''
Приветствую, {message.from_user.first_name}!
Это тестовый бот для FakeStoreAPI
Ваш chat_id: {message.chat.id}
Что я могу?
/help - переходите сюда
'''
    with sq.connect('message_ids.db') as con:
        cursor = con.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_ids(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        chat_id TEXT NOT NULL)''')
        cursor.execute(f'SELECT count(chat_id) FROM chat_ids WHERE chat_id = {message.chat.id}')
        isExist = cursor.fetchone()
        if isExist[0] == 0:
            cursor.execute('INSERT INTO chat_ids (username, chat_id) VALUES (?, ?)', (message.from_user.first_name, message.chat.id))

    bot.send_message(message.chat.id, mess)


print('bot started')
bot.infinity_polling()
