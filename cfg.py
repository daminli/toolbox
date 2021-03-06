import os

DATE_FORMAT='%Y/%m/%d'
TIME_FORMAT='%H:%M:%S'
DATETIME_FORMAT='%Y/%m/%d %H:%M:%S'
TIMESTAMP_FORMAT='%Y/%m/%d %H:%M:%S %f'

FREE_QUERY_EXP_DIR='D:\\mydoc\\Workspace\\flask_workspace\\toolbox_www'
FREE_QUERY_MIN_ZIP_SIZE='5'

class Config(object):
    DEBUG = True
    TESTING = False
    # available languages
    LANGUAGES = {
        'en': 'English',
        'zh': 'Chinese'
    }
    #SERVER_NAME='toolbox.local.com'
    #APPLICATION_ROOT='/toolbox'
    # slow database query threshold (in seconds)
    DATABASE_QUERY_TIMEOUT = 30
    CSRF_ENABLED = True
    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = 'welcome-to-my-planning-toolbox'
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:admin@localhost/postgres'
    SQLALCHEMY_MIGRATE_REPO=basedir+'\\db_repository'
    SQLALCHEMY_ECHO=False
    
    CACHE_TYPE='simple'
    
    JSON_DATETIME_FORMAT=DATETIME_FORMAT
    JSON_DATE_FORMAT=DATE_FORMAT
    JSON_TIME_FORMAT=TIME_FORMAT
    JSON_USE_ENCODE_METHODS=True
    
    
    UPLOAD_FOLDER = 'D:\\mydoc\\Workspace\\flask_workspace\\toolbox\\test\\uploads'
    ALLOWED_EXTENSIONS = set(['xlsx','xls','txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    MAX_CONTENT_LENGTH = 64 * 1024 * 1024  #64M

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    

class TestingConfig(Config):
    TESTING = True