import pytest
import requests
from app.users import users_list


@pytest.fixture()
def upload_data():
    r = requests.get('http://127.0.0.1:5000/users')
    return r.text
