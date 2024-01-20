# эта программа требует подключения 3 модулей: flask_db.py, User_login.py, forms.py

from flask import Flask
from flask import render_template, url_for, request, flash, session, redirect, abort, g, make_response
import sqlite3 as sq
import os
from forms import SuggessionForm, LogIn, Register
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from User_login import UserLogin
from flask_db import Fl_db

DATABASE = 'flask_db.db'
DEBUG = True
SECRET_KEY = 'fdgdfgdfggf786hfg6hfg6h7f'
MAX_CONTENT_LENGTH = 1024 * 1024

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flask_db.db')))

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Авторизуйтесь для доступа к закрытым страницам'

@login_manager.user_loader
def load_user(user_id):
    print('load user')
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    conn = sq.connect(app.config['DATABASE'])
    conn.row_factory = sq.Row
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = Fl_db(db)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


menu = [{'name': 'Главная', 'url': '/'},
        {'name': 'О нас', 'url': '/about'},
        {'name': 'Пожелания', 'url': '/suggestions'},
        {'name': 'Авторизация', 'url': '/login'},
        {'name': 'Регистрация', 'url': '/register'}]


@app.route('/')
def index():
    return render_template('index.html', title='Главное', menu=menu)


@app.route('/about')
def about():
    return render_template('about.html', menu=menu)


@app.route('/suggestions', methods=['GET', 'POST'])
@login_required
def create_ticket():
    form = SuggessionForm()
    if request.method == 'GET':
        return render_template('suggestions.html', menu=menu, form=form)

    if form.validate_on_submit():
        username = form.username.data
        e_mail = form.e_mail.data
        suggestion = form.suggestion.data
        dbase.create_table_suggestions()
        dbase.insert_suggestions(username, e_mail, suggestion)
    return render_template('suggestions.html', menu=menu, form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()
    if form.validate_on_submit():

        psw_hash = generate_password_hash(form.psw.data)
        dbase.create_table_users()
        dbase.insert_users(form.username.data, form.e_mail.data, psw_hash)
        flash('Вы успешно авторизованы!')
    return render_template('register.html', menu=menu, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogIn()
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if form.validate_on_submit():
        user = dbase.get_user_by_email(form.e_mail.data)
        if user and check_password_hash(user['password'], form.psw.data):
            userlogin = UserLogin().create(user)
            rm = True if form.remember.data else False
            login_user(userlogin, remember=rm)
            return redirect(request.args.get(("next")) or url_for('profile'))
        flash('Неверная пара логин/пароль', 'error')

    return render_template('login.html', menu=menu, form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    return render_template('profile.html', menu=menu)


@app.route('/userava')
@login_required
def userava():
    img = current_user.getAvatar(app)
    if not img:
        return ''

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and current_user.verifyExt(file.filename):
            try:
                img=file.read()
                res = dbase.updateUserAvatar(img, current_user.get_id())
                if not res:
                    flash('Ошибка обновления аватара', 'error')
                flash('Аватар обновлен')
            except FileNotFoundError as e:
                flash('Ошибка чтения файла')
        else:
            flash('Ошибка обновления аватара')
    return redirect(url_for('profile'))


if __name__ == '__main__':
    app.run(debug=True)
