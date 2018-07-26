import psycopg2
import psycopg2.extras

from flask_restful import abort

from flaskr.db import connectDB

from flaskr.models.user import User
from flaskr.resources.helpers import current_user


class Ride:
    """A representation of a ride.
    :param date: A string, the date the ride is to be taken.
    :param time: A string, the time the ride is to start.
    :param pickup: A string, the place where the ride starts.
    :param dropoff: A string, the destination of the ride.
    :param driver_id: An int, the unique identifier of the driver of the ride.
    :param price: A string, the price of the ride.
    :param status: A string, the status of the ride.
    """
    STATUS_IN_OFFER = 'In Offer'
    STATUS_STARTED = 'Started'
    STATUS_DONE = 'Done'
    STATUS_OPTIONS = [STATUS_IN_OFFER, STATUS_STARTED, STATUS_DONE]

    def __init__(self, date, time, pickup, dropoff, price, status=STATUS_IN_OFFER):
        from flaskr.models.car import Car
        car = Car.get_by_user_id(current_user())
        car_capacity = car['capacity']

        self.date = date
        self.time = time
        self.pickup = pickup
        self.dropoff = dropoff
        self.capacity = car_capacity
        self.seats_available = car_capacity
        self.price = price
        self.status = status
        self.driver_id = current_user()


    @staticmethod
    def browse():
        """A method to get all rides.
        :return: A list of dictionaries with all rides
        """
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM ride;')
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        ride_list = cursor.fetchall()
        cursor.close()
        connection.close()
        if len(ride_list) == 0:
            return {'status': 'success', 'message': 'There are no rides offers yet'}, 404
        else:
            data = []
            for ride in ride_list:
                item = {
                    'id': ride['id'],
                    'time': ride['time'],
                    'date': ride['date'],
                    'pickup': ride['pickup'],
                    'dropoff': ride['dropoff'],
                    'capacity': ride['capacity'],
                    'seats_available': ride['seats_available'],
                    'driver': User.read(ride['driver_id'])['fullname'],
                    'price': ride['price'],
                    'status': ride['status']
                }
                data.append(item)
            return {'status': 'success', 'message': 'Fetch successful', 'data': data}, 200

    @staticmethod
    def read(ride_id):
        """
        A method to get the details of a ride.
        :param ride_id: An int, the unique identifier of the ride.
        :return: ride details
        """
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM ride WHERE id = %s;',
                           ([int(ride_id)]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = cursor.fetchone()
        cursor.close()
        connection.close()
        if results is None:
            abort(
                404, message='The ride with id {} does not exist'.format(ride_id)
                )
        ride = {
            'id': results['id'],
            'time': results['time'],
            'date': results['date'],
            'pickup': results['pickup'],
            'dropoff': results['dropoff'],
            'capacity': results['capacity'],
            'seats_available': results['seats_available'],
            'driver': User.read(results['driver_id'])['fullname'],
            'price': results['price'],
            'status': results['status'],
            'requests': Ride.get_requests(ride_id)
        }
        return ride

    @staticmethod
    def edit(date, time, pickup, dropoff, price, status, ride_id):
        """
        A method to edit a ride's details.
        :param date: A string, the date the ride is to be taken.
        :param time: A string, the time the ride is to start.
        :param pickup: A string, the place where the ride starts.
        :param dropoff: A string, the destination of the ride.
        :param price: A string, the price of the ride.
        :param status: A string, the status of the ride.
        :param ride_id: An int, the unique identifier of the ride.
        :return: Http Response
        """
        Ride.is_ride_owner(ride_id)
        if status in Ride.STATUS_OPTIONS:
            from flaskr.models.car import Car
            car = Car.get_by_user_id(current_user())
            car_capacity = car['capacity']

            connection = connectDB()
            cursor = connection.cursor(
                cursor_factory=psycopg2.extras.DictCursor)
            Ride.abort_if_ride_offer_doesnt_exist(ride_id)
            try:
                cursor.execute(
                    """UPDATE ride SET 
                        date = %s,
                        time = %s,
                        pickup = %s,
                        dropoff = %s,
                        capacity = %s,
                        driver_id = %s,
                        price = %s,
                        status = %s
                    WHERE id = %s AND driver_id = %s;""",
                    (
                        date,
                        time,
                        pickup,
                        dropoff,
                        car_capacity,
                        current_user(),
                        price,
                        status,
                        ride_id,
                        current_user()
                    )
                )
                connection.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                connection.rollback()
                return {'status': 'failed', 'data': error}, 500
            cursor.close()
            connection.close()
            return {'status': 'success', 'data': 'Ride offer successfully updated'}, 200
        return {'status': 'failed', 'message': 'You entered an invalid ride status'}, 404

    def add(self):
        """
        A method to create a ride.
        :return: Http Response
        """
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute(
                """INSERT INTO ride (
                    date,
                    time,
                    pickup, 
                    dropoff,
                    capacity,
                    seats_available,
                    driver_id,
                    price,
                    status
                    ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""",
                (
                    self.date,
                    self.time,
                    self.pickup,
                    self.dropoff,
                    self.capacity,
                    self.seats_available,
                    self.driver_id,
                    self.price,
                    self.status
                )
            )
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'message': error}, 500
        cursor.close()
        connection.close()
        return {'status': 'success', 'message': 'Ride created successfully'}, 201

    @staticmethod
    def delete(ride_id):
        """
        A method to delete a ride.
        :param ride_id: An int, the unique identifier of the ride.
        :return: Http Response
        """
        Ride.is_ride_owner(ride_id)
        Ride.abort_if_ride_offer_doesnt_exist(ride_id)
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('DELETE FROM ride WHERE id = %s AND driver_id = %s;',
                                ([ride_id, current_user()]))
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        Ride.delete_this_rides_requests(ride_id)
        cursor.close()
        connection.close()
        return {'status': 'success', 'data': 'Ride request successfully deleted'}, 200

    @staticmethod
    def delete_this_rides_requests(ride_id):
        """
        A method to delete a ride's requests.
        :param ride_id: An int, the unique identifier of the ride.
        :return: Http Response
        """
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('DELETE FROM ride_request WHERE ride_id = %s ;',
                                ([ride_id]))
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        cursor.close()
        connection.close()
        return {'status': 'success', 'data': 'Ride requests successfully deleted'}, 200

    @staticmethod
    def abort_if_ride_offer_doesnt_exist(ride_id):
        """
        A method to check if a ride  exists.
        :param ride_id: An int, the unique identifier of the ride.
        :return: Http Response
        """
        return Ride.read(ride_id)

    @staticmethod
    def is_ride_owner(ride_id):
        """
        A method to check if a ride  exists.
        :param ride_id: An int, the unique identifier of the ride.
        :return: Http Response
        """
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM ride WHERE id = %s AND driver_id = %s;',
                           ([int(ride_id), current_user()]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = cursor.fetchone()
        cursor.close()
        connection.close()
        if results is None:
            abort(404, message='You do not have permission for this ride')
        return True

    @staticmethod
    def get_requests(ride_id):
        """
        A method to a ride's requests.
        :param ride_id: An int, the unique identifier of the ride.
        :return: Http Response
        """
        from flaskr.models.request import RideRequest
        return RideRequest.browse(ride_id)

