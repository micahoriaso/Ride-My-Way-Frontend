import os
import psycopg2
import psycopg2.extras
from urllib.parse import urlparse
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def connectDB():
    db_uri = os.environ.get(
        'DATABASE_URL', default='postgresql://oriaso:root100@127.0.0.1:5432/ride_my_way')
    connection_string = urlparse(db_uri)
    username = connection_string.username
    password = connection_string.password
    hostname = connection_string.hostname
    database = connection_string.path[1:]
    try:
        return psycopg2.connect(dbname=database, user=username, password=password, host=hostname)
    except:
        print('Can\'t connect to database')

def create_db_tables():
    queries = [
        'DROP TABLE IF EXISTS "ride" CASCADE',
        'DROP TABLE IF EXISTS "ride_request" CASCADE',
        'DROP TABLE IF EXISTS "app_user" CASCADE',
        'DROP TABLE IF EXISTS "car" CASCADE',
        """
        CREATE TABLE ride (
            id SERIAL PRIMARY KEY NOT NULL, 
            time VARCHAR(140) NOT NULL, 
            date VARCHAR(140) NOT NULL, 
            pickup VARCHAR(140) NOT NULL, 
            dropoff VARCHAR(140) NOT NULL, 
            capacity INT NOT NULL, 
            seats_available INT NOT NULL, 
            driver_id INT NOT NULL, 
            price REAL NOT NULL, 
            status VARCHAR(140) NOT NULL
            );
        """,
        """
        CREATE TABLE ride_request (
            id SERIAL PRIMARY KEY NOT NULL, 
            ride_id INT NOT NULL, 
            requestor_id INT NOT NULL, 
            request_status VARCHAR(140) NOT NULL
            );
        """,
        """
        CREATE TABLE app_user (
            id SERIAL PRIMARY KEY NOT NULL, 
            firstname VARCHAR(140) NOT NULL, 
            lastname VARCHAR(140) NOT NULL, 
            fullname VARCHAR(140) NOT NULL, 
            email VARCHAR(140) NOT NULL, 
            phone_number VARCHAR(140), 
            password VARCHAR(140) NOT NULL, 
            car_registration VARCHAR(140)
            );
        """,
        """
        CREATE TABLE car (
            id VARCHAR(140) PRIMARY KEY NOT NULL, 
            model VARCHAR(140) NOT NULL, 
            capacity INT NOT NULL,
            owner INT NOT NULL);
        """
    ]
    run_query_commands(queries)

def run_query_commands(queries):
    connection = None
    try:
       connection = connectDB()
       cursor = connection.cursor()
       for query in queries:
            cursor.execute(query)
       cursor.close()
       connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()


if __name__ == '__main__':
    create_db_tables()