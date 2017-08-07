import os
basedir = os.path.abspath(os.path.dirname(__file__))

CLIENT_ID = 'RQXWHQF5GMY4TPWCGOTTS41UFI2BNNTSVT5GCHPGU1WWCPLH'
CLIENT_SECRET = 'H2UY4GL3TARHBSK4F012XGHC5EKWCZXX1M5MHA1SDTOVZEJU'


class Config:
    SECRET_KEY = 'n#avz%e=lig@=*lxpk=3@$p)iol)2ge8^#w8h1-iks*yb9k@4j'
    CSRF_ENABLED = True


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = os.environ.get('DEBUG') or True


class StagingConfig(Config):
    DEBUG = os.environ.get('DEBUG') or True
    TESTING = True
    MONGODB_DB = 'meetneattest'
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


config = {
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}