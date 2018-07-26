import datetime
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash

from flask_jwt_extended import create_access_token

from flask_restful import abort

from flaskr.db import connectDB


class User:
    """A representation of a user.
    :param firstname: A string, the firstname of the user.
    :param lastname: A string, the lastname of the user.
    :param email: A string, the email address of the user.
    :param password: A string, the password of the user.
    :param phone_number: A string, the phone number of the user.
    :param car_registration: A string, the licence plate of the user's car.
    """
    def __init__(self, firstname, lastname, email, password, phone_number=None, car_registration=None):
        self.firstname = firstname
        self.lastname = lastname
        self.fullname = '{} {}'.format(firstname, lastname)
        self.email = email
        self.phone_number = phone_number
        self.password = generate_password_hash(
            password,
            method='sha256'
        )
        self.car_registration = car_registration

    @staticmethod
    def read(user_id):
        """A method to get all details of a user.
        :param user_id: An int, a unique identifier of the user.
        :return: user details
        """
        connection = connectDB()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM app_user WHERE id = %s ;',
                           ([user_id]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = cursor.fetchone()
        cursor.close()
        connection.close()
        if results is None:
            abort(404, message='The user with id {} does not exist'.format(user_id))
        user = {
            'id': results['id'],
            'firstname': results['firstname'],
            'lastname': results['lastname'],
            'fullname': results['fullname'],
            'email': results['email'],
            'phone_number': results['phone_number'],
            'password': results['password'],
            'car_registration': results['car_registration']
        }
        return user

    @staticmethod
    def edit(user_id, firstname, lastname, password, phone_number=None, car_registration=None):
        """
        A method to accept/decline a ride request.
        :param firstname: A string, the firstname of the user.
        :param lastname: A string, the lastname of the user.
        :param password: A string, the password of the user.
        :param phone_number: A string, the phone number of the user.
        :param car_registration: A string, the licence plate of the user's car.
        :return: Http Response
        """
        connection = connectDB()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        User.abort_if_user_doesnt_exist(user_id)
        try:
            cursor.execute(
                """UPDATE app_user SET
                    firstname = %s,
                    lastname = %s,
                    fullname = %s,
                    phone_number = %s,
                    password = %s,
                    car_registration = %s
                WHERE id = %s;""",
                (
                    firstname,
                    lastname,
                    '{} {}'.format(
                        firstname, lastname
                    ),
                    phone_number,
                    generate_password_hash(
                        password,
                        method='sha256'
                    ),
                    car_registration,
                    int(user_id)
                )
            )
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        cursor.close()
        connection.close()
        return {'status': 'success', 'message': 'User updated successfully'}, 200

    def add(self):
        """
        A method to create a user.
        :return: Http Response
        """
        connection = connectDB()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        User.abort_if_email_is_already_used(self.email)
        try:
            cursor.execute(
                """INSERT INTO app_user (
                    firstname,
                    lastname,
                    fullname,
                    email,
                    phone_number,
                    password,
                    car_registration
                    )
                VALUES (%s, %s, %s, %s, %s, %s, %s);""",
                (
                    self.firstname,
                    self.lastname,
                    self.fullname,
                    self.email,
                    self.phone_number,
                    self.password,
                    self.car_registration
                )
            )
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'message': error}, 500
        expires = datetime.timedelta(days=1)
        access_token = create_access_token(
            identity=self.email, expires_delta=expires)
        cursor.close()
        connection.close()
        return {
            'status': 'success', 
            'message': 'Account creation successful',
            'access_token': access_token,
            }, 201

    @staticmethod
    def login(email, password):
        """
        A method to login a user.
        :param email: A string, the email address of the user.
        :param password: A string, the password of the user.
        :return: Http Response
        """
        connection = connectDB()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM app_user WHERE email = %s ;',
                                ([email]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = cursor.fetchone()
        cursor.close()
        connection.close()
        if results is not None:
            if results['email'] == email and check_password_hash(results['password'], password):
                expires = datetime.timedelta(days=1)
                access_token = create_access_token(
                    identity=email, expires_delta=expires)
                return {
                    'status': 'success',
                    'message': 'Login successful',
                    'access_token': access_token,
                }, 200
            return {'status': 'failed', 'message': 'Wrong password, please try again'}, 401
        else:
            abort(401, message='The user with email {} does not exist'.format(
                email))

    @staticmethod
    def delete(user_id):
        """
        A method to delete a user.
        :param user_id: An int, the unique identifier of the user.
        :return: Http Response
        """
        connection = connectDB()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        User.abort_if_user_doesnt_exist(user_id)
        try:
            cursor.execute('DELETE FROM app_user WHERE id = %s ;',
                                ([user_id]))
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'message': error}, 200
        cursor.close()
        connection.close()
        return {'status': 'success', 'message': 'User successfully deleted'}, 200

    @staticmethod
    def abort_if_user_doesnt_exist(user_id):
        """
        A method to check if a  user exists.
        :param user_id: An int, the unique identifier of the user.
        :return: Http Response
        """
        return User.read(user_id)

    @staticmethod
    def abort_if_email_is_already_used(email):
        """
        A method to check if an email address is already used.
        :param email: A string, the email address of the user.
        :return: Http Response
        """
        connection = connectDB()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM app_user WHERE email = %s ;',
                                ([email]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = cursor.fetchone()
        cursor.close()
        connection.close()
        if results is not None:
            abort(400, message='The email {} is already taken'.format(email))
        return results

    @staticmethod
    def get_by_email(email):
        """A method to get all details of a user.
        :param email: A string, a unique email address for the user.
        :return: user id
        """
        connection = connectDB()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute('SELECT * FROM app_user WHERE email = %s ;',
                           ([email]))
        except (Exception, psycopg2.DatabaseError) as error:
            connection.rollback()
            return {'status': 'failed', 'data': error}, 500
        results = cursor.fetchone()
        cursor.close()
        connection.close()
        if results is None:
            abort(404, message='The user with email {} does not exist'.format(email))
        return results['id']
