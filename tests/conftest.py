import pytest
from app import app
from app.users import users_list


@pytest.fixture()
def request_to_server():

    def _set_route(route):
        client = app.test_client()
        res = client.get(route)
        return res.get_json()

    return _set_route


@pytest.fixture()
def request_to_db():
    return users_list
