[![Build Status](https://travis-ci.org/micahoriaso/Ride-My-Way.svg?branch=ft-ride-offers-api-158459164)](https://travis-ci.org/micahoriaso/Ride-My-Way)
[![Coverage Status](https://coveralls.io/repos/github/micahoriaso/Ride-My-Way/badge.svg?branch=master)](https://coveralls.io/github/micahoriaso/Ride-My-Way?branch=master)

# Ride-My-Way
Ride-My-Way App is a carpooling application that provides drivers with the ability to create ride offers and passengers to join available ride offers.

# Screenshot
![fireshot capture 007 - ride detail - file____home_oriaso_desktop_python_ride-my-way_ui_profile html](https://user-images.githubusercontent.com/20840601/41377320-6472fa3e-6f64-11e8-9a09-fcbdfd4eb886.png)

# Installation
* Clone the repo from github
```
https://github.com/micahoriaso/Ride-My-Way.git
```
* Create a virtual environment and activate it
```
python3 -m venv venv
source venv/bin/activate
```
* Install all dependencies

```
pip install -r requirements.txt
```
* Run the Flask application
```
flask run
```
# Testing
To test run the command 
```
pytest
```
# Endpoints

Endpoint | Functionality 
------------ | -------------
POST /api/v2/auth/signup | Signs up a user
POST /api/v2/auth/login | Logs in up a user
GET /api/v2/users/<user_id> | Gets details of a user
DELETE /api/v2/users/<user_id> | Deletes a user
PUT /api/v2/users/<user_id> | Updates a user's details
POST   /api/v2/cars | Create a car
GET   /api/v2/cars | Get all cars
GET   /api/v2/cars/<car_registration> | Get a single car
PUT   /api/v2/cars/<car_registration> | Update a single car
DELETE   /api/v2/cars/<car_registration> | Delete a car
POST   /api/v2/rides | Create a ride offer
GET   /api/v2/rides | Get all rides
GET   /api/v2/rides/<ride_id> | Get a single ride offer
PUT   /api/v2/rides/<ride_id> | Update a single ride offer
DELETE   /api/v2/rides/<ride_id> | Delete a ride offer
POST   /api/v2/rides/<ride_id>/requests | Create a request for a particular ride
GET   /api/v2/rides/<ride_id>/requests | Get all requests for a particular ride
GET   /api/v2/rides/<ride_id>/requests/<request_id> | Get a ride request
PUT  /api/v2/rides/<ride_id>/requests/<request_id> | Update a ride request
DELETE   /api/v2/rides/<ride_id>/requests/<request_id> | Delete a single request

## User
You can signup, login, edit, update and delete a user.

### User sign up
Send a Json payload to the following endpoint
```
/api/v2/auth/signup
```
Example Json payload
```
{
    "firstname": "Micah",
    "lastname": "Oriaso",
    "email": "micah@oriaso.com",
    "password": "123456789",
    "confirm_password": "123456789"
}
```

### User log in
Send a Json payload to the following endpoint
```
/api/v2/auth/login
```
Example Json payload
```
{
    "email": "micah@oriaso.com",
    "password": "123456789",
}
```

### Editing a user
A user can be edited by sending a `PUT` request
with a Json payload  to the following endpoint. Make sure to have added at least one ride request
```
/api/v2/users/<user_id>
```
e.g.
```
/api/v2/users/1
```
Json payload
```
{
    "firstname": "Micah",
    "lastname": "Oriaso",
    "password": "123456789",
    "car_registration": "KAA 540H",
    "phone_number": "0707896325"
}
```
### Delete a user
To delete a user, send a `DELETE`
request to the following endpoint. Make sure to have added at least one user
```
/api/v2/users/<user_id>
```
e.g.
```
/api/v2/users/1
```
## Cars

### Create a car

Below is an example of a request to create a car. 
```
/api/v2/cars/
```
Payload
```
{
    "registration": "KAA 540H",
    "model": "Mazda Speed 6",
    "capacity": "4",
}
```

The following response will be returned
```
{
    "status": "success",
    "message": "Car created successfully"
}
```

### Get ride offers
Below is an example of a *get* request endpoint to get the all cars

```
/api/v2/cars/
```
### Get a single car
To get a car by itd registration use, in doing so, make sure you have added atleast one car
```
/api/v2/car/<registration>
```
eg
```
/api/v2/cars/KAA 504H
```
The following response will be returned.
```
{
    "status": "success",
    "message": "Fetch successful",
    "data": {
    "registration": "KAA 540H",
    "model": "Mazda Speed 6",
    "capacity": "4",
    }
}
```

### Edit a ride offer
Send a `PUT` request in this syntax, make sure to have added at least one car
```
/api/v2/cars/<registration>
```
e.g.
```
/api/v2/cars/KAA 540H
```
Payload
```
{
    "model": "Mazda Speed",
    "capacity": "4",
}
```

### Delete a Ride Offer
Send a `Delete`request with the car's registration as shown below. Make sure to have added at least one car
```
/api/v2/cars/<registration>
```
e.g.
```
/api/v2/rides/KAA 540H
```

## Rides

### Create A ride

Below is an example of a request to create a ride. 
```
/api/v2/rides/
```
Payload
```
{
    "date": "2018-12-06",
    "time": "11:00",
    "pickup": "Nyayo Stadium",
    "dropoff": "Belle Vue",
    "price": "100",
    "driver_id": 1,
}
```

The following response will be returned
```
{
    "status": "success",
    "data": {
        "pickup": "Nyayo Stadium",
        "available_seats": 3,
        "id": 1,
        "date": "2018-12-06",
        "time": "11:00",
        "price": 100.0,
        "dropoff": "Belle Vue",
        "capacity": 3,
        "registration": "KAA 987I",
        "ride_status": "In Offer",
        "driver": "Farrell Williams",
        "car": "Mazda MX5"
    }
}
```

### Get ride offers
Below is an example of a *get* request endpoint to get the all ride offers

```
/api/v2/rides/
```
### Get a ride offer by id
To get a ride offer its id by use, in doing so, make sure you have added atleast on ride offer
```
/api/v2/rides/<ride_id>
```
eg
```
/api/v2/rides/1
```
The following response will be returned.
```
{
    "status": "success",
    "data": {
        "pickup": "Nyayo Stadium",
        "available_seats": 3,
        "id": 1,
        "date": "2018-12-06",
        "time": "11:00",
        "price": 100.0,
        "dropoff": "Belle Vue",
        "capacity": 3,
        "registration": "KAA 987I",
        "ride_status": "In Offer",
        "driver": "Farrell Williams",
        "car": "Mazda MX5"
    }
}
```

### Edit a ride offer
Send a `PUT` request in this syntax, make sure to have added at least on ride offer
```
/api/v2/rides/<ride_id>
```
e.g.
```
/api/v2/rides/1
```
Payload
```
{
	"date": "2018-12-06",
    "time": "11:00",
    "pickup": "Nyayo Stadium",
    "dropoff": "Belle Vue",
    "price": "100",
    "driver_id": 1,
}
```

### Delete a Ride Offer
Send a `Delete`request with the ride Id as shown below. Make sure to have added at least on ride offer
```
/api/v2/rides/<ride_id>
```
e.g.
```
/api/v2/rides/1
```

## Ride Requests
You can also add, edit, update and delete ride requests.

### Get requests from a ride
Get all the requests of a ride by
specifying the ride id.
```
/api/v2/rides/<ride_id>/requests
```
e.g.
```
/api/v2/rides/1/requests
```

### Get request for a ride
Use the endpoint below, make sure to have added atleast one ride request
```
/api/v2/rides/<ride_id>/requests/<request_id>
```
e.g.

### Add request to ride
Send a Json payload to the following endpoint
```
api/v2/rides/<ride_id>/requests
```
e.g.
```
api/v2/rides/1/requests
```
Example Json payload
```
{
	"requestor_id": 3,
}
```

### Editing a ride request
A ride request can be edited by sending a `PUT` request
with a Json payload  to the following endpoint. Make sure to have added at least one ride request
```
/api/v2/rides/<ride_id>/requests/<request_id>
```
e.g.
```
/api/v2/rides/2/requests/1
```
Json payload
```
{
	"request_status": "Accepted"
}
```
### Delete a ride request
To delete a request from a ride offer, send a `DELETE`
request to the following endpoint. Make sure to have added at least one ride request
```
/api/v2/rides/<ride_id>/requests/<request_id>
```
e.g.
```
/api/v2/rides/2/requests/1
```

* API Demo [Ride My Way](http://ride-my-way-micah.herokuapp.com/apidocs/)

# Author
* **Micah Oriaso** [micahoriaso](https://github.com/micahoriaso)

## Acknowledgments

* Derrick Kipkorir [@Derrickkip](https://github.com/Derrickkip)
