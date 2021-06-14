from datetime import datetime


def test_duplicate_id(request_to_db):
    temp_set = set()
    for item in request_to_db:
        temp_set.add(item.id)
    assert len(temp_set) == len(request_to_db)


def test_null_data(request_to_db):
    for item in request_to_db:
        assert item.id and item.username and item.email and item.department and item.date_joined


def test_date_format(request_to_db):
    for item in request_to_db:
        assert datetime.strptime(item.date_joined, '%Y-%m-%dT%H:%M:%S')

