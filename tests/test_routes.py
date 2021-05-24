

class TestUsers:
    def test_without_param(self):
        pass

    def test_param_username(self):
        pass

    def test_param_departments(self):
        pass

    def test_double_param(self):
        pass


class TestDepartment:
    def test_without_param(self):
        pass

    def test_param_name(self):
        pass


class TestFirst:
    def test_any(self, upload_data):
        print(upload_data)
        assert True
