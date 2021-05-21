from flask import render_template, request
from app import app
from app import users as u


@app.route('/')
@app.route('/index')
def index():
    text = 'Test endpoint.'
    return render_template('index.html', text=text)


@app.route('/users')
@app.route('/users/<username>')
def users(username=None):
    temp_list = list()
    if request.args.get('username'):
        username = request.args.get('username')
    if request.args.get('department'):
        depart = request.args.get('department')
    if username:
        for user in u.users_list:
            if user['username'] == username:
                temp_list.append(user)
    else:
        temp_list = u.users_list
    return render_template('users.html', title='Users list', users=temp_list)


@app.route('/department')
def department():
    if request.args.get('name'):
        depart = request.args.get('name')
    return render_template('departments.html')
