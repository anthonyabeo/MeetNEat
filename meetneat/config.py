import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get('SECRET_KEY')

CSRF_ENABLED = True

DEBUG = os.environ.get('DEBUG')

TESTING = os.environ.get('TESTING')

# DATABASES
MONGODB_DB = os.environ.get('MONGODB_DB', 'meetneat')
MONGODB_HOST = os.environ.get('MONGODB_HOST', 'localhost')
MONGODB_PORT = os.environ.get('MONGODB_PORT', 27017)


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

FOURSQUARE_CREDENTIALS = {
    'CLIENT_ID': 'RQXWHQF5GMY4TPWCGOTTS41UFI2BNNTSVT5GCHPGU1WWCPLH',
    'CLIENT_SECRET': 'H2UY4GL3TARHBSK4F012XGHC5EKWCZXX1M5MHA1SDTOVZEJU'
}


GOOGLE_MAPS_API_KEY = 'AIzaSyBQqaotMNuCb3mlLysFsV2iphpcoBqVWh4'

