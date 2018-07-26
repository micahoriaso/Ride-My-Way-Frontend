import os

from flask import Flask

from flask_restful import Api

from flasgger import Swagger

from flask_jwt_extended import JWTManager

from flaskr.resources.requests import requests_bp
from flaskr.resources.rides import rides_bp
from flaskr.resources.users import users_bp
from flaskr.resources.cars import cars_bp
from flaskr.db import create_db_tables




def create_app():
    """
    Create an instance of the flask application
    """

    app = Flask(__name__)
    app.config['SWAGGER'] = {
        'title': 'Ride My Way',
        'uiversion': 3,
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
            }
        },
    }
    app.url_map.strict_slashes = False

    app.config['JWT_SECRET_KEY'] = "?JVN\x04*\x15\x0c.w\x01I\x11\xd1@Z\xfc\xc8#\xdf\xf4\x83\x93\xf8"

    Swagger(app)
    JWTManager(app)

    """
    Flask blueprints
    """
    app.register_blueprint(requests_bp)
    app.register_blueprint(rides_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(cars_bp)

    """
    Flask application commands
    """
    @app.cli.command('initdb')
    def initdb_command():
        """Initializes the database."""
        create_db_tables()
        print('Initialized the database.')

    if __name__ == '__main__':
        app.run(debug=True)
        
    return app
