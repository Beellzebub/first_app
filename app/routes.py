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
    connection = psycopg2.connect(user="postgres", password="postgres")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    sql_create_database = cursor.execute('CREATE DATABASE users')
    cursor.close()
    connection.close()
except errors.lookup('42P04'):
    print('The database has already been created.')

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/users')

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

from app.models import *

Base.metadata.create_all(bind=engine)


@app.route('/users', methods=['GET'])
def get_users_html():
    username = request.args.get('username')
    depart_name = request.args.get('department')
    response_from_db = Users.query.all()
    serialized_response = [user.serialize() for user in response_from_db]
    filtered_response = users_filter(serialized_response, username, depart_name)
    return render_template('users.html', title='Users list', users=filtered_response)


@app.route('/api/users/', methods=['GET'])
def get_users_api():
    username = request.args.get('username')
    depart_name = request.args.get('department')
    response_from_db = Users.query.all()
    serialized_response = [user.serialize() for user in response_from_db]
    filtered_response = users_filter(serialized_response, username, depart_name)
    return jsonify(filtered_response)


@app.route('/api/users/', methods=['POST'])
def post_users_api():
    new_user = Users(**request.json)
    session.add(new_user)
    session.commit()
    return 'User successfully added.', 201


@app.route('/api/users/<int:user_id>', methods=['PUT'])
def put_users_api(user_id):
    item = Users.query.filter(Users.id == user_id).first()
    new_info = request.json
    if not item:
        return 'Not user with this id', 204
    for key, value in new_info.items():
        setattr(item, key, value)
    session.commit()
    return 'Information about user successfully changed.', 202


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def del_users_api(user_id):
    item = Users.query.filter(Users.id == user_id).first()
    if not item:
        return 'Not user with this id', 204
    session.delete(item)
    session.commit()
    return 'User successfully deleted.', 202


@app.route('/department', methods=['GET'])
def get_department_html():
    depart_name = request.args.get('name')
    response_from_db = Users.query.all()
    serialized_response = [user.serialize() for user in response_from_db]
    filtered_response = depart_filter(serialized_response, depart_name)
    return render_template('departments.html', title='Departments list', users=filtered_response)


@app.route('/api/department/', methods=['GET'])
def get_department_api():
    depart_name = request.args.get('name')
    response_from_db = Users.query.all()
    serialized_response = [user.serialize() for user in response_from_db]
    filtered_response = depart_filter(serialized_response, depart_name)
    return jsonify(filtered_response)


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


def depart_filter(list_for_filter, depart_name=None):
    temp_list = list()
    for user in list_for_filter:
        if depart_name:
            if depart_name in user['department'] and user['department'] not in temp_list:
                temp_list.append(user['department'])
        else:
            if user['department'] not in temp_list:
                temp_list.append(user['department'])
    return temp_list
