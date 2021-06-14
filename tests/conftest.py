import pytest
from app import app
from app.models import Users
from app.users import users_list


@pytest.fixture()
def request_to_server():

    def _set_route(route):
        client = app.test_client()
        res = client.get(route)
        return res

    return _set_route


@pytest.fixture()
def request_to_db():
    return Users.query.all()


# t = [item.serialize() for item in Users.query.all() if item.username == f'Hulk']
# print(t)


# for user in Users.query.all():
#     print(user)
# print(len(Users.query.all()))
