import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask

from .__version__ import __version__

load_dotenv()

APP_ROOT = Path(__file__).parents[1]
STATIC_PATH = APP_ROOT / "static"
TEMPLATE_PATH = APP_ROOT / "templates"


def create_app() -> Flask:
    """Create and configure the app."""
    app = Flask(
        __name__,
        instance_relative_config=True,
        static_folder=str(STATIC_PATH),
        template_folder=str(TEMPLATE_PATH),
    )
    app.config.from_object(
        os.environ.get("APP_SETTINGS", "podcast_log.config.DefaultConfig")
    )

    app.config.setdefault(
        "SQLALCHEMY_DATABASE_URI", f"sqlite:///{app.instance_path}/db.sqlite3"
    )

    handler = logging.StreamHandler(sys.stdout)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    Path(app.instance_path).mkdir(exist_ok=True)

    from . import models

    models.init_app(app)

    from . import routes

    routes.init_app(app)

    from . import api

    api.init_app(app)

    return app
