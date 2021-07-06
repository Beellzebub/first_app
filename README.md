# WebApp - study project.
Веб сервис выполняющий хранение информации о пользователе (id, username, email, department, date_joined).

Реализованы CRUD методы протокола HTTP, фильтрация по пользователю и департаменту.

Веб сервис написан с использованием фреймворка Flask.

В качестве базы данных используется PostgreSQL 13.

Для написания тестов использовался фреймворк pytest.

> Endpoints:
* GET /users
	* /users?username={username}
	* /users?department={department}
	* /users?username={username}&department={department}
* GET /api/users/
	* /api/users/?username={username}
	* /api/users/?department={department}
	* /api/users/?username={username}&department={department}
* POST /api/users/
* PUT /api/users/{id}
* DELETE /api/users/{id}
* GET /department
	* /department?name={department)
* GET /api/department/
	* /api/department/?name={department)

> JSON for POST and PUT methods:
```
{
    "username": "Username",
    "email": "user@test.com",
    "department": "Department",
    "date_joined": "1912-06-23T09:00:00"
}
```

> Python library used:
* Flask
* SQLAlchemy
* pytest
* pytest-xdist
* psycopg2

> For start server use command:

`python app\main.py`

> For start tests use command:

`pytest tests` - запуск всех тестов.

`pytest -n2 tests` - параллельный запуск всех тестов в 2 потока.

> For start server in docker:

`docker build-t i_server ./app`

`docker run --name c_server --rm -p 5000:5000 -it i_server main.py`

> For start tests in docker:

`docker build -t i_tests .`

`docker run --name c_tests --rm -it i_tests`

> For start server and tests together:

`docker-compose build`

`docker-compose up`
