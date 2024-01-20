import sqlite3 as sq


class Fl_Db:
    def __init__(self, db):
        self.db = db

#     def create_table_newsletter(self):
#         cursor = self.db.cursor()
#         cursor.execute('''
# CREATE TABLE IF NOT EXISTS newsletter(
# id INTEGER PRIMARY KEY AUTOINCREMENT,
# username TEXT NOT NULL,
# message TEXT NOT NULL)''')

    def create_table_chat_ids(self):
        cursor = self.db.cursor()
        cursor.execute('''
CREATE TABLE IF NOT EXISTS chat_ids(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT NOT NULL,
chat_id TEXT NOT NULL)''')

    # def number_of_bot_users(self):
    #     cursor = self.db.cursor()
    #     cursor.execute('SELECT count(*) FROM chat_ids')
    #     num = cursor.fetchone()
    #     return num[0]

#     def insert_messages(self, username, message):
#         cursor = self.db.cursor()
#         cursor.execute('''
# INSERT INTO newsletter(username, message) VALUES(?, ?)''', (username, message))
#         self.db.commit()

#     def insert_chats(self, username, chat_id):
#         cursor = self.db.cursor()
#         cursor.execute('''
# INSERT INTO chat_ids(username, chat_id) VALUES(?, ?)''', (username, chat_id))
#         self.db.commit()

    def fetch_chat_ids(self):
        cursor = self.db.cursor()
        cursor.execute('SELECT chat_id FROM chat_ids')
        res = cursor.fetchall()
        lst = []
        for i in res:
            lst.append(i[0])
        return lst


# db1 = Fl_Db('flask_db.db')
# print(db1.fetch_chat_ids())
