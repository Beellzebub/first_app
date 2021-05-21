from flask import render_template
from app import app
from app import users as u


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/users')
def users():
    return render_template('users.html', title='Users list', users=u.users_dict)


@app.route('/department')
def department():
    return render_template('departments.html')
