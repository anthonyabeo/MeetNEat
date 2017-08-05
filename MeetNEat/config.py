import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'n#avz%e=lig@=*lxpk=3@$p)iol)2ge8^#w8h1-iks*yb9k@4j'
    CSRF_ENABLED = True
    OAUTH_CREDENTIALS = {

        'facebook': {
            'id': '111900076114805',
            'secret': '8e0cbe1dc9cbe489cd377d76e6bb10c3'
        },

        'twitter': {
            'id': 'woPymnfG1CdZq6eKIBoWUVRkB',
            'secret': 'gxHy3FsPN1jLYmDvO7Gm9Z99PSOwK5GXg9xf2in8NcRSbKhRNx'
        }

    }

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = os.environ.get('DEBUG') or True

class StagingConfig(Config):
    TESTING = True
    MONGOALCHEMY_DATABASE = 'meetneat'


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


config = {
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}