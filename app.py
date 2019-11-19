import babel
import dateutil.parser
import logging
from flask import Flask
from flask_moment import Moment
from logging import Formatter, FileHandler
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()
migrate = Migrate()
moment = Moment()


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    from views.artists import bp as artists_bp
    from views.main import bp as main_bp
    from views.shows import bp as shows_bp
    from views.venues import bp as venues_bp

    app.register_blueprint(artists_bp, url_prefix="/artists")
    app.register_blueprint(main_bp, url_prefix="/")
    app.register_blueprint(shows_bp, url_prefix="/shows")
    app.register_blueprint(venues_bp, url_prefix="/venues")

    def format_datetime(value, _format="medium"):
        date = dateutil.parser.parse(value)
        if _format == "full":
            _format = "EEEE MMMM, d, y 'at' h:mma"
        elif _format == "medium":
            _format = "EE MM, dd, y h:mma"
        return babel.dates.format_datetime(date, _format, locale="en_US")

    app.jinja_env.filters["datetime"] = format_datetime

    if not app.debug:
        file_handler = FileHandler("error.log")
        file_handler.setFormatter(
            Formatter(
                "%(asctime)s %(levelname)s: %(message)s "
                "[in %(pathname)s:%(lineno)d]"
            )
        )
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info("errors")

    return app
