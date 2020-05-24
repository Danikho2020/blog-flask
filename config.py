from decouple import config

class Config:
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'my_secret_key'
    #SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/flask_1'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/flask_3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = 'my_secret_key'
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL', default='localhost')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}