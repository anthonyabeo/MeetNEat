import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret key'
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
    pass


config = {
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}