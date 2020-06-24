class BaseConfig():
    API_PREFIX = '/api'
    TESTING = False
    DEBUG = False


class Development(BaseConfig):
    FLASK_ENV = 'development'
    DEBUG = True


class Production(BaseConfig):
    FLASK_ENV = 'production'


class Test(BaseConfig):
    FLASK_ENV = 'development'
    TESTING = True
    DEBUG = True
