"""Various application configurations."""

import os


class DefaultConfig:
    """Base configuration storing default values."""

    DEVELOPMENT = False
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "this-really-needs-to-be-changed"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI: str  # Set in __init__.py or in config class.


class ProductionConfig(DefaultConfig):
    """Configuration for production deployment."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "")
    # SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}/{}".format(
    #     os.environ.get("RDS_USERNAME"),
    #     os.environ.get("RDS_PASSWORD"),
    #     os.environ.get("RDS_HOSTNAME"),
    #     os.environ.get("RDS_DB_NAME"),
    # )


class StagingConfig(DefaultConfig):
    """Configuration for staging deployment."""

    DEBUG = True


class DevelopmentConfig(DefaultConfig):
    """Configuration for local development."""

    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(DefaultConfig):
    """Configuration for testing."""

    TESTING = True
    SECRET_KEY = "test"
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    WTF_CSRF_ENABLED = False
