import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'n#avz%e=lig@=*lxpk=3@$p)iol)2ge8^#w8h1-iks*yb9k@4j'
    CSRF_ENABLED = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = os.environ.get('DEBUG') or True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                                'sqlite:///' + os.path.join(basedir, 'DB-dev.sqlite')


class StagingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'DB-dev.sqlite')


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


config = {
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}