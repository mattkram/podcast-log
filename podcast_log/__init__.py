import logging
import os
import sys
from pathlib import Path

from flask import Flask

STATIC_PATH = Path(__file__).parents[1] / "static"
TEMPLATE_PATH = Path(__file__).parents[1] / "templates"


def create_app():
    # create and configure the app
    app = Flask(
        __name__,
        instance_relative_config=True,
        static_folder=STATIC_PATH,
        template_folder=TEMPLATE_PATH,
    )
    app.config.from_object(
        os.environ.get("APP_SETTINGS", "podcast_log.config.DefaultConfig")
    )

    if app.config["SQLALCHEMY_DATABASE_URI"] is None:
        app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = f"sqlite:///{app.instance_path}/db.sqlite3"

    handler = logging.StreamHandler(sys.stdout)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    Path(app.instance_path).mkdir(exist_ok=True)

    from . import models

    models.init_app(app)

    from . import views

    views.init_app(app)

    # models.create_db(app)

    return app
