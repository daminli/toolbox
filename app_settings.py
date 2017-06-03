import os
class Config(object):
    DEBUG = True
    TESTING = False
    # available languages
    LANGUAGES = {
        'en': 'English',
        'zh': 'Chinese'
    }
    # slow database query threshold (in seconds)
    DATABASE_QUERY_TIMEOUT = 30
    CSRF_ENABLED = True
    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = 'welcome-to-my-planning-toolbox'
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:admin@localhost/postgres'
    SQLALCHEMY_MIGRATE_REPO=basedir+'\\db_repository'
    SQLALCHEMY_ECHO=True
    
    CACHE_TYPE='simple'
    DATE_FORMAT='%Y/%m/%d'
    TIME_FORMAT='%H:%M:%S'
    DATETIME_FORMAT='%Y/%m/%d %H:%M:%S'
    TIMESTAMP_FORMAT='%Y/%m/%d %H:%M:%S %f'
    
    JSON_USE_ENCODE_METHODS=True

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    

class TestingConfig(Config):
    TESTING = True