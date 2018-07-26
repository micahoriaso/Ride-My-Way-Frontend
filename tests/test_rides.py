import pytest, json

import flaskr
from flaskr.resources.helpers import get_db_rows


@pytest.fixture
def test_case_data(client, auth_header, header):
    data = {
        '1': {
            'date': '2018-06-12',
            'time': '11:00',
            'pickup': 'Nyayo Estate',
            'dropoff': 'Belle Vue',
            'price': '100',
        },
        '4':{
            'date': '2018-06-12',
            'time': '11:00',
            'pickup': 'Nyayo Stadium',
            'dropoff': 'Belle Vue',
            'price': '100',
            },
        '5': {
            "firstname": "Sharon",
            "lastname": "Paul",
            "email": "sp@gmail.com",
            "password": "10101010",
            "confirm_password": "10101010"
        },
        '6': {
            'registration': 'KAA 540H',
            'model': 'Nissan GTR',
            'capacity': '2',
        },
        '7': {
            "firstname": "Sharon",
            "lastname": "Paul",
            "password": "10101010",
            "car_registration": "KAA 540H",
            "phone_number": "0707896325"
        },
        '8': {
            'date': '2018-06-12',
            'time': '11:00',
            'pickup': 'Nyayo Stadium',
            'dropoff': 'Belle Vue',
            'price': '100',
            'capacity': '3',
            'available_seats': '1',
            'driver_id': 1,
            'car': 'Mazda MX5',
            'registration': 'KAA 987I',
            'status': 'Completed'
        },
    }

    client.post(
        '/api/v2/auth/signup',
        data=json.dumps(data['5']), 
        headers=header
        )

    client.post(
        '/api/v2/cars/',
        data=json.dumps(data['6']),
        headers=auth_header
    )

    return data


def test_get_empty_ride_offer(client, test_case_data, auth_header):
    response = client.get('/api/v2/rides/',
                          headers=auth_header)
    response_data = response.get_json()
    assert response.status_code == 404
    assert response_data['message'] == 'There are no rides offers yet'

def test_add_new_ride_offer(client, test_case_data, auth_header):
    pre_insert_rows = get_db_rows('select * from ride;')
    response = client.post('/api/v2/rides/', 
                           data=json.dumps(test_case_data['4']), headers=auth_header)
    post_insert_rows = get_db_rows('select * from ride;')
    
    assert len(post_insert_rows) == len(pre_insert_rows) + 1
    assert response.status_code == 201

def test_get_all_rides(client, auth_header):
    response = client.get('/api/v2/rides/', headers=auth_header)
    assert response.status_code == 200

def test_get_one_available_ride(client, test_case_data, auth_header):
    response = client.post('/api/v2/rides/', 
                           data=json.dumps(test_case_data['4']), headers=auth_header)
    response = client.get('/api/v2/rides/1', headers=auth_header)
    assert response.status_code == 200

def test_get_one_unavailable_ride(client, auth_header):
    response = client.get('/api/v2/rides/555', headers=auth_header)
    assert response.status_code == 404


def test_edit_existing_ride_offer(client, test_case_data, auth_header):
    response = client.put('/api/v2/rides/1', 
                          data=json.dumps(test_case_data['1']), headers=auth_header)
    assert response.status_code == 200


def test_edit_ride_offer_with_invalid_status(client, test_case_data, auth_header):
    response = client.put(
        '/api/v2/rides/1',
        data=json.dumps(test_case_data['8']),
        headers=auth_header
    )
    response_data = response.get_json()
    assert response.status_code == 404
    assert response_data['message'] == 'You entered an invalid ride status'

def test_delete_existing_ride(client, auth_header):
    pre_delete_rows = get_db_rows('select * from ride;')
    response = client.delete('/api/v2/rides/1', headers=auth_header)
    post_delete_rows = get_db_rows('select * from ride;')

    assert len(post_delete_rows) == len(pre_delete_rows) - 1
    assert response.status_code == 200

def test_delete_nonexistent_ride(client, auth_header):
    pre_delete_rows = get_db_rows('select * from ride;')
    response = client.delete('/api/v2/rides/555', headers=auth_header)
    post_delete_rows = get_db_rows('select * from ride;')

    assert len(post_delete_rows) == len(pre_delete_rows)
    assert response.status_code == 404
