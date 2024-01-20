from flask import Flask, session
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'e69de628f3c00c61a8d39c30c63d899ddbabb031'
app.permanent_session_lifetime = datetime.timedelta(days=10)


@app.route("/")
def index():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1
    return f"<h1>Main page</h1><p>Число просмотров: {session['visits']}"


data = [1, 2, 3, 4]
@app.route("/session")
def session_data():
    session.permanent = True
    if 'data' not in session:
        session['data'] = data
    else:
        session['data'][1] += 1
        session.modified = True

    return f"<p>session['data']: {session['data']}"



if __name__ == "__main__":
    app.run(debug=True)
