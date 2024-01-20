import sqlite3 as sq

class Fl_db:
    def __init__(self, db):
        self.db = db
        self.cursor = db.cursor()

    def create_table_suggestions(self):
        self.cursor.execute('''
    CREATE TABLE IF NOT EXISTS suggestions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    suggestion TEXT NOT NULL)''')
        self.db.commit()

    def insert_suggestions(self, username, email, suggestion):
        self.cursor.execute('''
    INSERT INTO suggestions(username, email, suggestion) VALUES(?, ?, ?)''', (username, email, suggestion))
        self.db.commit()

    def create_table_users(self):
        self.cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    avatar BLOB DEFAULT NULL)''')

    def insert_users(self, username, email, password):
        self.cursor.execute('''
    INSERT INTO users(username, email, password) VALUES(?, ?, ?)''', (username, email, password))
        self.db.commit()

    def getUser(self, user_id):
        try:
            self.cursor.execute('SELECT * FROM users WHERE id =? LIMIT 1', user_id)
            res = self.cursor.fetchone()
            if not res:
                print('Пользователь не найден')
                return False
            return res
        except sq.Error as e:
            print('Ошибка получения данных из БД' + str(e))
        return False

    def get_user_by_email(self, e_mail):
        self.cursor.execute(f'''
    SELECT * FROM users WHERE email LIKE "{e_mail}" LIMIT 1''')
        res = self.cursor.fetchone()
        return res

    def updateUserAvatar(self, avatar, user_id):
        if not avatar:
            return False

        try:
            binary = sq.Binary(avatar)
            self.cursor.execute(f'UPDATE users SET avata = ? WHERE id = ?', binary, user_id)
            self.db.commit()
        except sq.Error as e:
            print('Ошибка обновления аватара в БД '+ str(e))
            return False
        return True
