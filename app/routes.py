from flask import render_template, request
from app import app
from app.users import users_list


@app.route('/users')
def users():
    """
    Create endpoint /users contains list of users.
    Filters (can used together):
        -username (partial or complete match).
        -department (complete match).
    If matches not found - show empty page.
    :return: users.html
    """
    temp_list = list()
    username = request.args.get('username')
    depart_name = request.args.get('department')

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

    return render_template('users.html', title='Users list', users=temp_list)


@app.route('/department')
def department():
    """
    Create endpoint /department contains list of departments.
    Filter:
        -name (partial or complete match).
    If matches not found - show empty page.
    :return: departments.html
    """
    temp_list = list()
    depart_name = request.args.get('name')

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

    return render_template('departments.html', title='Departments list', users=temp_list)
