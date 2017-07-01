import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from MeetNEat import create_app, db
from api.models import User, Request, Proposal, MealDate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Request=Request, Proposal=Proposal, MealDate=MealDate)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()