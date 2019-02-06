import os

basedir = os.path.abspath(os.path.dirname(__file__))


class DefaultConfig(object):
    DEVELOPMENT = False
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "this-really-needs-to-be-changed"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(DefaultConfig):
    DEVELOPMENT = False
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}/{}".format(
        os.environ.get("RDS_USERNAME"),
        os.environ.get("RDS_PASSWORD"),
        os.environ.get("RDS_HOSTNAME"),
        os.environ.get("RDS_DB_NAME"),
    )


class StagingConfig(DefaultConfig):
    DEVELOPMENT = False
    DEBUG = True


class DevelopmentConfig(DefaultConfig):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(DefaultConfig):
    TESTING = True
    SECRET_KEY = "test"
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    WTF_CSRF_ENABLED = False
