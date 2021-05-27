class TestUsers:
    def test_get_request(self, request_to_server):
        assert request_to_server('/api/users/').status_code == 200
        assert request_to_server('/users/').status_code == 200

    def test_without_param(self, request_to_server, request_to_db):
        assert len(request_to_server('/api/users/').get_json()) == len(request_to_db)

    def test_param_username(self, request_to_server, request_to_db):
        user = 'Tony'
        req = f'/api/users/?username={user}'
        assert request_to_server(req).get_json() == [item for item in request_to_db
                                                     if item['username'] == 'Tony']

    def test_param_departments(self, request_to_server, request_to_db):
        department = 'frontend'
        req = f'/api/users/?department={department}'
        assert request_to_server(req).get_json() == [item for item in request_to_db
                                                     if item['department'] == 'frontend']

    def test_double_param(self, request_to_server, request_to_db):
        user = 'Bruce'
        department = 'frontend'
        req = f'/api/users/?username={user}&department={department}'
        assert request_to_server(req).get_json() == [item for item in request_to_db
                                                     if item['department'] == 'frontend' and item['username'] == 'Bruce']


class TestDepartment:
    def test_get_request(self, request_to_server):
        assert request_to_server('/api/department/').status_code == 200
        assert request_to_server('/department/').status_code == 200

    def test_without_param(self, request_to_server, request_to_db):
        depart_list = list()
        for item in request_to_db:
            if item['department'] not in depart_list:
                depart_list.append(item['department'])
        assert len(request_to_server('/api/department/').get_json()) == len(depart_list)

    def test_param_name(self, request_to_server, request_to_db):
        department = 'fullstack'
        req = f'/api/department/?name={department}'
        depart_list = list()
        for item in request_to_db:
            if item['department'] not in depart_list and item['department'] == 'fullstack':
                depart_list.append(item['department'])
        assert request_to_server(req).get_json() == depart_list
