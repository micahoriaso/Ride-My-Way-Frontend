import pytest, json

import flaskr
from flaskr.resources.helpers import get_db_rows

@pytest.fixture
def test_case_data():
    data = {
        '1': {
            'registration': 'KAA 540H',
            'model': 'Nissan GTR',
            'capacity': '2',
            },
        '2':{
            'model': 'BMW M5',
            'capacity': '3',
            },
        '3': {
            'registration': 'KAB 540H',
            'model': 'Nissan GTR',
            'capacity': '0',
            },
        '4': {
            'registration': 'KAA 540H',
            'model': 'Nissan GTR',
            'capacity': '0',
            }
        }
    return data


def test_get_cars_from_empty_table(client, test_case_data, auth_header):
    response = client.get('/api/v2/cars/', 
                           headers=auth_header)
    response_data = response.get_json()
    assert response.status_code == 202
    assert response_data['message'] == 'There are no cars here'

def test_add_new_car(client, test_case_data, auth_header):
    pre_insert_rows = get_db_rows('select * from car;')
    response = client.post('/api/v2/cars/', 
                           data=json.dumps(test_case_data['1']), headers=auth_header)
    post_insert_rows = get_db_rows('select * from car;')
    assert response.status_code == 201
    assert len(post_insert_rows) == len(pre_insert_rows) + 1

def test_get_all_cars(client, auth_header):
    response = client.get('/api/v2/cars/', headers=auth_header)
    assert response.status_code == 200

def test_get_one_available_car(client, test_case_data, auth_header):
    client.post('/api/v2/cars/', 
                           data=json.dumps(test_case_data['1']), headers=auth_header)
    response = client.get('/api/v2/cars/KAA 540H', headers=auth_header)
    assert response.status_code == 200

def test_get_one_unavailable_car(client, auth_header):
    response = client.get('/api/v2/cars/555', headers=auth_header)
    assert response.status_code == 404

def test_edit_existing_car(client, test_case_data, auth_header):
    response = client.put('/api/v2/cars/KAA 540H',
                          data=json.dumps(test_case_data['2']), headers=auth_header)
    assert response.status_code == 200

def test_edit_car_with_zero_capacity(client, test_case_data, auth_header):
    pre_insert_rows = get_db_rows('select * from car;')
    response = client.put('/api/v2/cars/KAA 540H',
                           data=json.dumps(test_case_data['4']), headers=auth_header)
    post_insert_rows = get_db_rows('select * from car;')
    response_data = response.get_json()
    assert response.status_code == 202
    assert len(post_insert_rows) == len(pre_insert_rows)
    assert response_data['message'] == 'Car capacity cannot be below one'

def test_delete_nonexistent_car(client, auth_header):
    pre_delete_rows = get_db_rows('select * from app_user;')
    response = client.delete('/api/v2/cars/555', headers=auth_header)
    post_delete_rows = get_db_rows('select * from app_user;')

    assert len(post_delete_rows) == len(pre_delete_rows)
    assert response.status_code == 404

def test_delete_existing_car(client, auth_header):
    pre_delete_rows = get_db_rows('select * from car;')
    response = client.delete('/api/v2/cars/KAA 540H', headers=auth_header)
    post_delete_rows = get_db_rows('select * from car;')
    
    assert len(post_delete_rows) == len(pre_delete_rows) - 1
    assert response.status_code == 200


def test_add_car_with_zero_capacity(client, test_case_data, auth_header):
    pre_insert_rows = get_db_rows('select * from car;')
    response = client.post('/api/v2/cars/',
                           data=json.dumps(test_case_data['3']), headers=auth_header)
    post_insert_rows = get_db_rows('select * from car;')
    response_data = response.get_json()
    assert response.status_code == 202
    assert len(post_insert_rows) == len(pre_insert_rows)
    assert response_data['message'] == 'Car capacity cannot be below one'

