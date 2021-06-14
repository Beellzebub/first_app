import pytest


class TestUsers:
    def test_get_request(self, request_to_server):
        assert request_to_server('/api/users/').status_code == 200
        assert request_to_server('/users').status_code == 200

    def test_without_param(self, request_to_server, request_to_db):
        assert len(request_to_server('/api/users/').get_json()) == len(request_to_db)

    @pytest.mark.parametrize('user', ['Tony', 'Bruce'])
    def test_param_username(self, request_to_server, request_to_db, user):
        req = f'/api/users/?username={user}'
        assert request_to_server(req).get_json() == [item.serialize() for item in request_to_db
                                                     if item.username == f'{user}']

    @pytest.mark.parametrize('dep', ['frontend', 'fullstack'])
    def test_param_departments(self, request_to_server, request_to_db, dep):
        req = f'/api/users/?department={dep}'
        assert request_to_server(req).get_json() == [item.serialize() for item in request_to_db
                                                     if item.department == f'{dep}']

    @pytest.mark.parametrize('user, dep', [('Tony', 'fullstack'), ('Bruce', 'frontend')])
    def test_double_param(self, request_to_server, request_to_db, user, dep):
        req = f'/api/users/?username={user}&department={dep}'
        assert request_to_server(req).get_json() == [item for item in request_to_db
                                                     if item.department == f'{dep}' and item.username == f'{user}']

    def test_post_request(self, request_to_server, test_user):
        test_data = {
            'username': 'Steve',
            'email': 'user2@test.com',
            'department': 'frontend',
            'date_joined': '2020-01-20T09:00:00'
        }
        assert request_to_server('/api/users/', 'POST', test_data).status_code == 201

    def test_put_request(self, request_to_server, test_user):
        test_data = {
            'username': 'Thor',
            'department': 'backend'
        }
        user_id = test_user.id
        assert request_to_server(f'/api/users/{user_id}', 'PUT', test_data).status_code == 202

    def test_delete_request(self, request_to_server, test_user):
        user_id = test_user.id
        assert request_to_server(f'/api/users/{user_id}', 'DELETE').status_code == 202


class TestDepartment:
    def test_get_request(self, request_to_server):
        assert request_to_server('/api/department/').status_code == 200
        assert request_to_server('/department').status_code == 200

    def test_without_param(self, request_to_server, request_to_db):
        depart_list = list()
        for item in request_to_db:
            if item.department not in depart_list:
                depart_list.append(item.department)
        assert len(request_to_server('/api/department/').get_json()) == len(depart_list)

    @pytest.mark.parametrize('dep', ['frontend', 'fullstack'])
    def test_param_name(self, request_to_server, request_to_db, dep):
        req = f'/api/department/?name={dep}'
        depart_list = list()
        for item in request_to_db:
            if item.department not in depart_list and item.department == f'{dep}':
                depart_list.append(item.department)
        assert request_to_server(req).get_json() == depart_list
