from flask import render_template, request, jsonify
from app import app
from app.users import users_list


@app.route('/users/', methods=['GET'])
def users():
    """
    Create endpoint /users contains list of users.
    Filters (can used together):
        -username (partial or complete match).
        -department (complete match).
    If matches not found - show empty page.
    :return: users.html
    """
    username = request.args.get('username')
    depart_name = request.args.get('department')
    final_list = users_filter(username, depart_name)
    return render_template('users.html', title='Users list', users=final_list)


@app.route('/api/users/', methods=['GET'])
def users_api():
    """

    :return: json
    """
    username = request.args.get('username')
    depart_name = request.args.get('department')
    final_list = users_filter(username, depart_name)
    return jsonify(final_list)


@app.route('/department/', methods=['GET'])
def department():
    """
    Create endpoint /department contains list of departments.
    Filter:
        -name (partial or complete match).
    If matches not found - show empty page.
    :return: departments.html
    """
    depart_name = request.args.get('name')
    final_list = depart_filter(depart_name)
    return render_template('departments.html', title='Departments list', users=final_list)


@app.route('/api/department/', methods=['GET'])
def department_api():
    """

    :return:
    """
    depart_name = request.args.get('name')
    final_list = depart_filter(depart_name)
    return jsonify(final_list)


def depart_filter(depart_name):
    """

    :param depart_name:
    :return:
    """
    temp_list = list()
    for user in users_list:
        if depart_name:
            if depart_name in user['department']:
                for temp_user in temp_list:
                    if temp_user['department'] == user['department']:
                        break
                else:
                    temp_list.append(user)
        else:
            for temp_user in temp_list:
                if temp_user['department'] == user['department']:
                    break
            else:
                temp_list.append(user)
    return temp_list


def users_filter(username=None, depart_name=None):
    """

    :param username:
    :param depart_name:
    :return:
    """
    temp_list = list()
    for user in users_list:
        if username and depart_name:
            if username.lower() in user['username'] and depart_name == user['department']:
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
