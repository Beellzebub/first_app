import logging

import pytest
from app import app
from app.routes import Base, engine, session as db_session
from app.models import Users


@pytest.fixture(scope='function')
def test_app():
    _app = app
    Base.metadata.create_all(bind=engine)
    _app.connection = engine.connect()

    yield app

    _app.connection.close()


@pytest.fixture(scope='function')
def session(test_app):

    yield db_session

    db_session.close_all()


@pytest.fixture(scope='function')
def test_user(session):
    user = Users(
        username='TestUser',
        email='Test@test.ru',
        department='TestDepartment',
        date_joined='2020-01-20T09:00:00'
    )
    session.add(user)
    session.commit()

    yield user


# @pytest.fixture(scope='function')
# def clean_user(session):
#
#     yield
#
#     session.delete(user)
#     session.commit()


@pytest.fixture()
def request_to_server():

    def _set_route(route, method='GET', data=dict):
        client = app.test_client()
        if method == 'GET':
            return client.get(route)
        if method == 'POST':
            return client.post(route, json=data)
        if method == 'PUT':
            return client.put(route, json=data)
        if method == 'DELETE':
            return client.delete(route)

    return _set_route


@pytest.fixture()
def request_to_db():
    return Users.query.all()


@pytest.fixture(autouse=True)
def good_message():
    print('Good test always', end=' ')


@pytest.fixture(scope='function', autouse=True)
def logs_start_info(request, logs_failed_info):
    logging.info(request.node.nodeid)


@pytest.fixture(scope='session')
def logs_failed_info(request):
    logging.info('Start tests:')
    yield
    logging.info('Last failed:')
    key = r'cache\lastfailed'
    failed_dict = request.config.cache.get(key, {})
    for failed_test in failed_dict.keys():
        logging.info(failed_test)

