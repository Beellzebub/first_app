from flask import render_template, request, jsonify
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app import app
from app.users import users_list
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
from psycopg2 import errors

try:
    connection = psycopg2.connect(user="postgres", password="112233")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    sql_create_database = cursor.execute('CREATE DATABASE users')
    cursor.close()
    connection.close()
except errors.lookup('42P04'):
    print('The database has already been created.')

engine = create_engine('postgresql+psycopg2://postgres:112233@localhost:5432/users')

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

from models import *

Base.metadata.create_all(bind=engine)


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
    response_from_db = Users.query.all()
    serialized = []
    for user in response_from_db:
        serialized.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'department': user.department,
            'date_joined': user.date_joined
        })
    final_list = users_filter(serialized, username, depart_name)
    return jsonify(final_list)


@app.route('/api/users/', methods=['POST'])
def post_users_api():
    new_one = Users(**request.json)
    session.add(new_one)
    session.commit()
    return 'User successfully added.', 201


@app.route('/api/users/<int:user_id>', methods=['PUT'])
def put_users_api(user_id):
    idx, item = next((x for x in enumerate(users_list) if x[1]['id'] == user_id), (None, None))
    new_info = request.json
    if not item:
        return 'Not user with this id', 204
    users_list[idx].update(new_info)
    return 'Information about user successfully changed.', 202


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def del_users_api(user_id):
    idx, item = next((x for x in enumerate(users_list) if x[1]['id'] == user_id), (None, None))
    if not item:
        return 'Not user with this id', 204
    users_list.pop(idx)
    return 'User successfully deleted.', 202


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


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


def users_filter(list_for_filter, username=None, depart_name=None):
    temp_list = list()
    for user in list_for_filter:
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
