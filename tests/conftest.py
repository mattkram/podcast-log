import os

import pytest
from podcast_log import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# @pytest.fixture(scope="session")
# def django_db_use_migrations(request):
#     return True
#
#
# @pytest.fixture(scope="session")
# def django_db_setup():
#     settings.DATABASES["default"] = {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": os.path.join(BASE_DIR, "test_db.sqlite3"),
#     }
