class TestUsers:
    def test_without_param(self, request_to_server, request_to_db):
        assert len(request_to_server('/api/users/')) == len(request_to_db)

    def test_param_username(self, request_to_server, request_to_db):
        assert request_to_server('/api/users/?username=To') == [item for item in request_to_db
                                                                if item['username'] == 'Tony']

    def test_param_departments(self, request_to_server, request_to_db):
        assert True

    def test_double_param(self, request_to_server, request_to_db):
        assert True


class TestDepartment:
    def test_without_param(self, request_to_server, request_to_db):
        assert True

    def test_param_name(self, request_to_server, request_to_db):
        assert True
