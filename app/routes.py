from flask import render_template, request, jsonify
from app import app
from app.users import users_list


@app.route('/users', methods=['GET'])
def get_users_html():
    username = request.args.get('username')
    depart_name = request.args.get('department')
    final_list = users_filter(username, depart_name)
    return render_template('users.html', title='Users list', users=final_list)


@app.route('/api/users/', methods=['GET'])
def get_users_api():
    username = request.args.get('username')
    depart_name = request.args.get('department')
    final_list = users_filter(username, depart_name)
    return jsonify(final_list)


@app.route('/api/users/', methods=['POST'])
def post_users_api():
    new_user = request.json
    users_list.append(new_user)
    return 'User successfully added.'


@app.route('/api/users/<user_id>', methods=['PUT'])
def put_users_api():
    return 'Information about user successfully changed.'


@app.route('/api/users/<user_id>', methods=['DELETE'])
def del_users_api():
    return 'User successfully deleted.'


@app.route('/department', methods=['GET'])
def get_department_html():
    depart_name = request.args.get('name')
    final_list = depart_filter(depart_name)
    return render_template('departments.html', title='Departments list', users=final_list)


@app.route('/api/department/', methods=['GET'])
def get_department_api():
    depart_name = request.args.get('name')
    final_list = depart_filter(depart_name)
    return jsonify(final_list)


def users_filter(username=None, depart_name=None):
    temp_list = list()
    for user in users_list:
        if username and depart_name:
            if username in user['username'] and depart_name == user['department']:
                temp_list.append(user)
        elif username:
            if username in user['username']:
                temp_list.append(user)
        elif depart_name:
            if depart_name == user['department']:
                temp_list.append(user)
        else:
            temp_list.append(user)
    return temp_list


def depart_filter(depart_name=None):
    temp_list = list()
    for user in users_list:
        if depart_name:
            if depart_name in user['department'] and user['department'] not in temp_list:
                temp_list.append(user['department'])
        else:
            if user['department'] not in temp_list:
                temp_list.append(user['department'])
    return temp_list
