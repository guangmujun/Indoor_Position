from flask_script import Manager

from indoor_position import create_app, db

manager = Manager(create_app)

@manager.command
def createdb(drop_first=False):
    if drop_first:
        db.drop_all()
    db.create_all()


if __name__ == '__main__':
    manager.run()
