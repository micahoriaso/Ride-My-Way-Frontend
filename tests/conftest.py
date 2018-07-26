import pytest, json

from flaskr import create_app
from flaskr.db import create_db_tables

@pytest.fixture
def app():
    app = create_app()
    yield app


@pytest.fixture()
def client(app, setup):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(scope='module')
def setup(request):
    create_db_tables()

    def teardown():
        create_db_tables()
    request.addfinalizer(teardown)


@pytest.fixture
def auth_header(client):
    data = {
        '1': {
            "firstname": "Micah",
            "lastname": "Oriaso",
            "email": "micahoriaso@gmail.com",
            "password": "10101010",
            "confirm_password": "10101010"
        },
        '2': {
            "email": "micahoriaso@gmail.com",
            "password": "10101010",
        },
    }
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    client.post(
        '/api/v2/auth/signup',
        data=json.dumps(data['1']),
        headers=headers
    )
    login_user = client.post(
        '/api/v2/auth/login',
        data=json.dumps(data['2']),
        headers=headers
    )
    response_data = login_user.get_json()
    access_token = response_data['access_token']

    authorization = 'Bearer ' + access_token
    headers_with_auth = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': authorization
    }
    return headers_with_auth


@pytest.fixture
def header():
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    return headers