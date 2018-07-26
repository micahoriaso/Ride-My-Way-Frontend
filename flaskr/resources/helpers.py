import re, datetime

import psycopg2
import psycopg2.extras


from flask_restful import abort

from flaskr.db import connectDB


def match_email(email):
    email_pattern = re.compile(
        '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
        )

    return email_pattern.match(email)

def strip_whitespace(string):
    return string.replace(" ", "")

def check_for_empty_fields(args):
    for k, v in args.items():
        if isinstance(v, str):
            v =strip_whitespace(v)
            if v == "":
                abort(500, message='Please fill in the field {}'.format(k))

def check_if_integer(args):
    try:
        args = int(args)
    except ValueError:
        # it was a string, not an int.
        abort(500, message='{} should be a number'.format(args))

def validate_date(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        abort(500, message='Date should be of the format YYYY-MM-DD')


def get_db_rows(query):
    connection = connectDB()
    cursor = connection.cursor(
        cursor_factory=psycopg2.extras.DictCursor)
    try:
        cursor.execute(query)
    except (Exception, psycopg2.DatabaseError) as error:
        connection.rollback()
        return {'status': 'failed', 'data': error}, 500
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def current_user():
    from flask_jwt_extended import get_jwt_identity
    from flaskr.models.user import User
    
    return User.get_by_email(get_jwt_identity())
