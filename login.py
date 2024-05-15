import sys

from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps

from DB import DB

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'  # Change this to a secure random key

# Define dummy user credentials (replace with your actual authentication logic)
users = {'user1': 'password1', 'user2': 'password2'}


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # print(username," ",password)
    db = DB()
    userf = db.info(username, password)
    # print(username, " ", password)
    # print(userf)

    if userf == 1:
        return render_template('user.html')
    else:
        return render_template('login.html', message='Invalid username or password')


@app.route('/success')
@login_required
def success():
    username = session['username']
    return f'Welcome, {username}!'


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
