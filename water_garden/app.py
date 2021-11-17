"""The app module, containing the app factory function."""
from flask import Flask
from flask_bootstrap import Bootstrap
from water_garden import views

from water_garden.extensions import (
    db,
    login_manager,
)


def create_app():
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """
    print(__name__.split(".")[0])
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
    Bootstrap(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my_plants.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    print(__name__.split(".")[0])
    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    login_manager.init_app(app)
    return None

def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(views.blueprint)
    return None

