from flask import Flask
from flask import render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fdgdfgdfggf786hfg6hfg6h7f'

msg = ''
menu = [{'name': 'Главная', 'url': '/'},
        {'name': 'О нас', 'url': 'about'},
        {'name': 'FAQ', 'url': 'faq'},
        {'name': 'Донаты', 'url': 'donates'},
        {'name': 'Обратная связь', 'url': 'feedback'}]


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
    global msg
    if request.method == 'POST':
        msg = request.form['message']
    return render_template('feedback.html', title='Обратная связь', menu=menu)


# @app.route('/contact', methods=["POST", "GET"])
# def contact():
#     # print(url_for('index'))
#     if request.method == "POST":
#         if len(request.form['username']) > 2:
#             flash('Сообщение отправлено', category='success')
#         else:
#             flash('Ошибка отправки', category='error')
#
#     return render_template('contact.html', title='Обратная связь', menu=menu)
#
#
# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     if 'userLogged' in session:
#         return redirect(url_for('profile', username=session['userLogged']))
#     elif request.method == 'POST' and request.form['username'] == 'selfedu' and request.form['psw'] == '123':
#         session['userLogged'] = request.form['username']
#         return redirect(url_for('profile', username=session['userLogged']))
#
#     return render_template('login.html', title='Авторизация', menu=menu)
#
#
# @app.route('/profile/<username>')
# def profile(username):
#     if 'userLogged' not in session or session['userLogged'] != username:
#         abort(401)
#     return f'Профиль пользователя {username}'
#
#
# @app.errorhandler(404)
# def pageNotFound(error):
#     return render_template('page404.html', title='Страница не найдена', menu=menu), 404



if __name__ == '__main__':
    app.run(debug=True)

# with app.test_request_context():
#     print(msg)

