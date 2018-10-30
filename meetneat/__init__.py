from flask import Flask
from flask_login import LoginManager
from flask_mongoengine import MongoEngine

db = MongoEngine()
login_manager = LoginManager()

login_manager.session_protection = 'strong'
login_manager.login_view = 'admin.sign_in'


def create_app():
    app = Flask(__name__)
    app.config.from_object('meetneat.config')

    db.init_app(app)
    login_manager.init_app(app)

    from api import api_blueprint
    from admin import admin_blueprint

    app.register_blueprint(api_blueprint)
    app.register_blueprint(admin_blueprint)

    app.app_context().push()

    return app
