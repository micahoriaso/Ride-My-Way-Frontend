import psycopg2
import psycopg2.extras
from flask_jwt_extended import get_jwt_identity

from flask_restful import abort

from flaskr.db import connectDB
from flaskr.models.user import User
from flaskr.resources.helpers import current_user


class Car:
    """A representation of a car.

    :param registration: A string, the car's licence plate.
    :param model: An int, the car's model.
    :param capacity: An int, the car's passenger capacity.
    """
    def __init__(self, registration, model, capacity):
        self.registration = registration
        self.model = model
        self.capacity = capacity
        self.owner = current_user()


    @staticmethod
    def browse():
        """A method to get all cars.

        :return: A list of dictionaries with all rides
        """
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM car where owner = \'%s\';',
                           ([current_user()]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        car_list = cursor.fetchall()
        cursor.close()
        connection.close()
        if len(car_list) == 0:
            return {'status': 'success', 'message': 'There are no cars here'}, 202
        else:
            data = []
            for car in car_list:
                item = {
                'registration':car['id'],
                'model':car['model'],
                'capacity':car['capacity'],
                'owner': User.read(car['owner'])['fullname']
                }
                data.append(item)
            return {'status': 'success', 'message': 'Fetch successful', 'data': data}, 200

    @staticmethod
    def read(car_registration):
        """
        A method to get the details of a car.
        :param car_registration: string, The car's licence plate
        :return: car details
        """
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM car WHERE id = %s AND owner = %s;',
                           ([car_registration, current_user()]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = cursor.fetchone()
        cursor.close()
        connection.close()
        if results is None:
            abort(404, message='The car with licence plate  {} does not exist'.format(
                car_registration))
        car = {
            'registration': results['id'],
            'model': results['model'],
            'capacity': results['capacity'],
            'owner': User.read(results['owner'])['fullname']
        }
        return car

    @staticmethod
    def edit(car_registration, model, capacity):
        """
        A method to edit the details of a car.
        :param registration: A string, the car's licence plate.
        :param model: An int, the car's model.
        :param capacity: An int, the car's passenger capacity.
        :return: Http Response
        """
        Car.abort_if_car_doesnt_exist(car_registration)
        if Car.capacity_greater_than_zero(capacity):
            connection = connectDB()
            cursor = connection.cursor(
                cursor_factory=psycopg2.extras.DictCursor)
            try:
                cursor.execute(
                    """
                    UPDATE car SET 
                        model = %s,
                        capacity = %s
                    WHERE id = %s AND owner = %s;
                    """,
                    (
                        model,
                        capacity,
                        car_registration,
                        current_user()
                    )
                )
                connection.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                connection.rollback()
                return {'status': 'failed', 'data': error}, 500
            cursor.close()
            connection.close()
            return {'status': 'success', 'data': 'Car successfully updated'}, 200
        return {'status': 'failed', 'message': 'Car capacity cannot be below one'}, 202

    def add(self):
        """
        A method to create a car.
        :return: Http Response
        """
        Car.abort_if_car_registration_is_already_used(self.registration)
        Car.abort_if_user_has_car(self.owner)
        if Car.capacity_greater_than_zero(self.capacity):
            connection = connectDB()
            cursor = connection.cursor(
                cursor_factory=psycopg2.extras.DictCursor)
            try:
                cursor.execute(
                    """INSERT INTO car (id, model, capacity, owner) 
                    VALUES (%s, %s, %s, %s);""",
                    (self.registration, self.model, self.capacity, self.owner))
                connection.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                connection.rollback()
                return {'status': 'failed', 'data': error}, 500
            cursor.close()
            connection.close()
            return {'status': 'success', 'message': 'Car created successfully'}, 201
        return {'status': 'failed', 'message': 'Car capacity cannot be below one'}, 202

    @staticmethod
    def delete(car_registration):
        """
        A method to delete a car.
        :param registration: A string, the car's licence plate.
        :return: Http Response
        """
        Car.abort_if_car_doesnt_exist(car_registration)
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('DELETE FROM car WHERE id = %s AND owner = %s ;',
                           ([car_registration, current_user()]))
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        cursor.close()
        connection.close()
        return {'status': 'success', 'data': 'Car successfully deleted'}, 200
    
    @staticmethod
    def abort_if_car_registration_is_already_used(registration):
        """
        A method to check if a car's liceence plate is unique.
        :param registration: A string, the car's licence plate.
        :return: Http Response
        """
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM car WHERE id = %s ;',
                                ([registration]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = cursor.fetchone()
        cursor.close()
        connection.close()
        if results is not None:
            abort(400, message='The licence plate {} is already used'.format(
                registration))
        return results

    @staticmethod
    def abort_if_car_doesnt_exist(registration):
        """
        A method to check if a car exists in the database.
        :param registration: A string, the car's licence plate.
        :return: Http Response
        """
        return Car.read(registration)

    @staticmethod
    def abort_if_user_has_car(user_id):
        """
        A method to check if the user has a car in the database.
        :param user_id: An integer, a unique identification of the user.
        :return: Http Response
        """
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM car WHERE owner = %s ;',
                           ([user_id]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = cursor.fetchone()
        cursor.close()
        connection.close()
        if results is not None:
            abort(400, message='You already have a car, you do not need to add another one')
        return results

    @staticmethod
    def capacity_greater_than_zero(capacity):
        """
        A method to check if a car's capacity is greater than zero.
        :param capacity: An int, the car's passenger capacity.
        :return: Http Response
        """
        if capacity > 0:
            return True
        return False

    @staticmethod
    def get_by_user_id(user_id):
        """
        A method to get a car owned by a specific user.
        :param user_id: An integer, a unique identification of the user.
        :return: Http Response
        """
        connection = connectDB()
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM car WHERE owner = %s ;',
                           ([user_id]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = cursor.fetchone()
        cursor.close()
        connection.close()
        if results is None:
            abort(
                404, message='You have no car yet, enter your car details first to proceed')

        car = {
            'registration': results['id'],
            'model': results['model'],
            'capacity': results['capacity'],
            'owner': User.read(results['owner'])['fullname']
        }
        return car
