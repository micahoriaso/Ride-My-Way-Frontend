class BaseConfig:
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    DB_CONNECTION_STRING = 'dbname=ride_my_way user=oriaso password=root100 host=localhost'


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    DB_CONNECTION_STRING = 'dbname=ride_my_way user=oriaso password=root100 host=localhost'

class ProductionConfig(BaseConfig):
    DB_CONNECTION_STRING = 'dbname=d20a76hinjubmj user=ifchaudfsytatc password=620be74d604db55a40d8e886d88a4ee22c0ac251c21199c3fe35a3a2afe18a84 host=ec2-23-21-164-107.compute-1.amazonaws.com'

CONFIG ={
    'DEVELOPMENT': DevelopmentConfig,
    'TESTING': TestingConfig,
    'PRODUCTION': ProductionConfig,
}