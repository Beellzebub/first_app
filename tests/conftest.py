import logging
import datetime
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
    yield user


@pytest.fixture(scope='function')
def add_user(session, test_user):
    session.add(test_user)
    session.commit()


@pytest.fixture(scope='function')
def del_user(session, test_user):
    yield
    item = test_user.query.filter(test_user.username == 'TestUser').first()
    session.delete(item)
    session.commit()


@pytest.fixture(scope='function')
def add_and_del_user(session, test_user):
    session.add(test_user)
    session.commit()
    yield
    session.delete(test_user)
    session.commit()


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


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport():
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        logging.info('\nFailed:')
        logging.info(rep.nodeid)


@pytest.fixture(autouse=True)
def good_message():
    print('Good test always', end=' ')


@pytest.fixture(scope='function', autouse=True)
def logs_started_tests(request, logs_last_failed_info):
    logging.info(request.node.nodeid)


@pytest.fixture(scope='session')
def logs_last_failed_info(request):
    logging.info(f'[{datetime.datetime.today().strftime("%d-%m-%YT%H:%M:%S")}]')
    logging.info('Running tests:')
    yield
    logging.info('\nLast failed:')
    key = r'cache\lastfailed'
    failed_dict = request.config.cache.get(key, {})
    for failed_test in failed_dict.keys():
        logging.info(failed_test)
