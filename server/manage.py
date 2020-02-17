from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db

app.config.from_object('config.BaseConfig')  # or app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)  # provide a migration utility command


# enable python shell with application context
@manager.shell
def shell_ctx():
    return dict(app=app,
                db=db)


if __name__ == '__main__':
    manager.run()
