"""The app module, containing the app factory function."""
import os
from flask import Flask
from flask_bootstrap import Bootstrap
from water_garden import views
from apscheduler.schedulers.background import BackgroundScheduler
from water_garden.utils import watering_reminder

from water_garden.extensions import (
    db,
    login_manager,
)


def create_app():
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    Bootstrap(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my_plants.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    register_extensions(app)
    register_blueprints(app)

    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(watering_reminder, trigger="interval", days=1, args=[app])
    scheduler.start()
    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
    login_manager.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(views.blueprint)
    return None
