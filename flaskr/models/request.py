import psycopg2
import psycopg2.extras

from flask_restful import abort

from flaskr.db import connectDB
from flaskr.models.user import User
from flaskr.resources.helpers import current_user



class RideRequest:
    """A representation of a ride request.
    :param ride_id: An int, the unique identifier of a ride.
    :param requestor_id: An int, the unique identifier of a requestor.
    :param request_status: A string, the status of the ride request.
    """
    STATUS_REQUESTED = 'Requested'
    STATUS_ACCEPTED = 'Accepted'
    STATUS_DECLINED = 'Declined'
    STATUS_OPTIONS = [STATUS_REQUESTED, STATUS_ACCEPTED, STATUS_DECLINED]
    
    def __init__(self, ride_id, request_status=STATUS_REQUESTED, requestor_id=None):
        self.ride_id = ride_id
        self.request_status = request_status
        self.requestor_id = current_user()

    @staticmethod
    def browse(ride_id):
        """A method to get all ride requests.
        :return: A list of dictionaries with all ride requests
        """
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        RideRequest.abort_if_ride_offer_doesnt_exist(ride_id)
        try:
            cursor.execute('SELECT id, ride_id, requestor_id, request_status FROM ride_request WHERE ride_id = %s;',
                           ([ride_id]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        ride_offer_requests = cursor.fetchall()
        cursor.close()
        connection.close()
        if len(ride_offer_requests) == 0:
            return {'status': 'success', 'message': 'No requests available for this ride yet'}, 404
        else:
            data = []
            for request in ride_offer_requests:
                item = {
                    'id': request['id'],
                    'ride_id': request['ride_id'],
                    'requestor': User.read(request['requestor_id'])['fullname'],
                    'request_status': request['request_status'],
                }
                data.append(item)
            return {'status': 'success', 'message': 'Fetch successful', 'data': data}

    @staticmethod
    def read(ride_id, request_id):
        """
        A method to get the details of a ride request.
        :param ride_id: An int, the unique identifier of a ride.
        :param request_id: An int, the unique identifier of a ride request.
        :return: ride request details
        """
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        RideRequest.abort_if_ride_offer_doesnt_exist(ride_id)
        RideRequest.abort_if_ride_request_doesnt_exist(request_id)
        try:
            cursor.execute('SELECT * FROM ride_request WHERE id = %s ;',
                                ([request_id]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = cursor.fetchone()
        cursor.close()
        connection.close()
        request = {
            'id': results['id'],
            'ride_id': results['ride_id'],
            'requestor': User.read(results['requestor_id'])['fullname'],
            'request_status': results['request_status'],
        }
        return request, 200

    @staticmethod
    def edit(ride_id, request_id, request_status):
        """
        A method to accept/decline a ride request.
        :param ride_id: An int, the unique identifier of a ride.
        :param request_id: An int, the unique identifier of the ride request.
        :param request_status: A string, the status of the ride request.
        :return: Http Response
        """
        if request_status in RideRequest.STATUS_OPTIONS:
            connection = connectDB()
            cursor = connection.cursor(
                cursor_factory=psycopg2.extras.DictCursor)
            RideRequest.abort_if_ride_offer_doesnt_exist(ride_id)
            RideRequest.abort_if_ride_request_doesnt_exist(request_id)
            try:
                cursor.execute('UPDATE ride_request SET request_status = %s WHERE id = %s;',
                                    (request_status, request_id))

                connection.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                connection.rollback()
                return {'status': 'failed', 'data': error}, 500
            cursor.close()
            connection.close()
            if request_status == RideRequest.STATUS_DECLINED:
                RideRequest.increment_available_seats(ride_id)
            return {'status': 'success', 'data': 'Ride request successfully updated'}, 200
        return {'status': 'failed', 'message': 'You entered an invalid request status'}, 404

    def add(self):
        """
        A method to create a ride request.
        :return: Http Response
        """
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
    
        RideRequest.abort_if_ride_offer_doesnt_exist(self.ride_id)
        # RideRequest.abort_if_ride_owner(self.ride_id)
        RideRequest.abort_if_capacity_exceeded(self.ride_id)
        try:
            cursor.execute(
                """INSERT INTO ride_request (ride_id, requestor_id, request_status) 
                VALUES (%s, %s, %s);""",
                (self.ride_id, self.requestor_id, self.request_status))
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        cursor.close()
        connection.close()
        RideRequest.decrement_available_seats(self.ride_id)
        return {'status': 'success', 'message': 'Ride requested successfully'}, 201

    @staticmethod
    def delete(ride_id, request_id):
        """
        A method to delete a ride request.
        :param ride_id: An int, the unique identifier of a ride.
        :param request_id: An int, the unique identifier of the ride request.
        :return: Http Response
        """
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        RideRequest.abort_if_ride_offer_doesnt_exist(ride_id)
        RideRequest.abort_if_ride_request_doesnt_exist(request_id)
        RideRequest.is_request_owner(request_id)
        try:
            cursor.execute('DELETE FROM ride_request WHERE id = %s AND requestor_id = %s ;',
                                ([request_id, current_user()]))
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        cursor.close()
        connection.close()
        RideRequest.increment_available_seats(ride_id)
        return {'status': 'success', 'message': 'Ride request successfully deleted'}, 200

    @staticmethod
    def abort_if_ride_offer_doesnt_exist(ride_id):
        """
        A method to check if a  ride exists.
        :param ride_id: An int, the unique identifier of a ride.
        :return: Http Response
        """
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM ride WHERE id = %s;',
                           ([ride_id]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = cursor.fetchone()
        cursor.close()
        connection.close()
        if results is None:
            abort(404, message='The ride with id {} does not exist'.format(ride_id))
        return results

    @staticmethod
    def abort_if_ride_request_doesnt_exist(request_id):
        """
        A method to check if a ride request exists.
        :param request_id: An int, the unique identifier of a ride request.
        :return: Http Response
        """
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM ride_request WHERE id = %s ;',
                                ([request_id]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = cursor.fetchone()
        cursor.close()
        connection.close()
        if results is None:
            abort(404, message='The ride request with id {} does not exist'.format(request_id))
        return results

    @staticmethod
    def is_request_owner(request_id):
        """
        A method to check if a ride  exists.
        :param ride_id: An int, the unique identifier of the ride.
        :return: Http Response
        """
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM ride_request WHERE id = %s AND requestor_id = %s;',
                           ([int(request_id), current_user()]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = cursor.fetchone()
        cursor.close()
        connection.close()
        if results is None:
            abort(404, message='You do not have permission for this request')
        return True

    @staticmethod
    def abort_if_ride_owner(ride_id):
        """
        A method to check if the requestor is also the ride  owner.
        :param ride_id: An int, the unique identifier of the ride.
        :return: Http Response
        """
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM ride WHERE id = %s and driver_id = %s;',
                           ([ride_id, current_user()]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = cursor.fetchone()
        cursor.close()
        connection.close()
        if results is None:
            return True
        abort(404, message='You cannot request your own ride')

    @staticmethod
    def abort_if_capacity_exceeded(ride_id):
        """
        A method to check if the requestor is also the ride  owner.
        :param ride_id: An int, the unique identifier of the ride.
        :return: Http Response
        """
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM ride WHERE id = %s;',
                           ([ride_id]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = cursor.fetchone()
        cursor.close()
        connection.close()
        if results['seats_available'] < 1:
            abort(404, message='All seats for this ride have been taken')
        return True

    @staticmethod
    def abort_if_max_capacity_exceeded(ride_id):
        """
        A method to check if the requestor is also the ride  owner.
        :param ride_id: An int, the unique identifier of the ride.
        :return: Http Response
        """
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM ride WHERE id = %s;',
                           ([ride_id]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = cursor.fetchone()
        cursor.close()
        connection.close()
        if results['seats_available'] > results['capacity']:
            abort(404, message='Maximum ride capacity has been exceeded')
        return True

    @staticmethod
    def increment_available_seats(ride_id):
        """
        A method to check if the requestor is also the ride  owner.
        :param seats_available: An int, the number of seats available in a ride.
        :return: Http Response
        """
        from flaskr.models.ride import Ride
        seats_available = Ride.read(ride_id)['seats_available']
        seats_available += 1
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        RideRequest.abort_if_max_capacity_exceeded(ride_id)
        try:
            cursor.execute('UPDATE ride SET seats_available = %s WHERE id = %s;',
                           ([seats_available, ride_id]))
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return error
        cursor.close()
        connection.close()

    @staticmethod
    def decrement_available_seats(ride_id):
        """
        A method to check if the requestor is also the ride  owner.
        :param seats_available: An int, the number of seats available in a ride.
        :return: Http Response
        """
        from flaskr.models.ride import Ride
        seats_available = Ride.read(ride_id)['seats_available']
        seats_available -= 1
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('UPDATE ride SET seats_available = %s WHERE id = %s;',
                           ([seats_available, ride_id]))
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return error
        cursor.close()
        connection.close()
