import os

from flask_script import Manager, Shell

from MeetNEat import create_app, db
from api.models import User, Request, Proposal, MealDate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Request=Request, Proposal=Proposal, MealDate=MealDate)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()

