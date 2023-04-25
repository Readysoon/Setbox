from flask import Flask
from app.extensions.authentication import login_manager
from app.extensions.database.database import db, migrate
from app.config import Config
from . import subjects, lesson, schedule, user



def create_app(config_class=Config()):
    app = Flask(__name__)
    app.config.from_object(config_class)

    register_extensions(app)
    register_blueprints(app)
    login_manager.init_app(app)

    return app


def register_blueprints(app: Flask):
    app.register_blueprint(subjects.routes.blueprint)
    app.register_blueprint(lesson.routes.blueprint)
    app.register_blueprint(schedule.routes.blueprint)
    app.register_blueprint(user.routes.blueprint)


def register_extensions(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
