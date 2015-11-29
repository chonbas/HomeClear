import os
from app import create_app, db
from app.models import User, Listing, Tax, Crime, Geo, School, Image, Inject
from flask.ext.script import Manager, Shell, Server

app = create_app(os.getenv('HOMECLEAR_CONFIG') or 'default')
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db, User=User, Listing=Listing, Tax=Tax, Crime=Crime, Inject=Inject,Image=Image,Geo=Geo, School=School)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == "__main__":
    manager.run()
