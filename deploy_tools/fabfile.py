import os
import random
import string

from dotenv import load_dotenv
from invoke import run, task
from patchwork.files import append, exists

load_dotenv()

REPO_URL = os.environ["REPO_URL"]
PYTHON = "python3.7"


@task
def deploy(c):
    site_folder = f"/home/{c.user}/sites/{c.host}"
    c.run(f"mkdir -p {site_folder}")
    with c.cd(site_folder):
        _update_system_dependencies(c)
        _get_latest_source(c)
        _update_virtualenv(c)
        _create_or_update_dotenv(c)
        _update_database(c)


def _update_system_dependencies(connection):
    connection.run("sudo add-apt-repository ppa:deadsnakes/ppa --yes")
    connection.run("sudo apt-get update")

    packages = [
        # "software-properties-common",
        # PYTHON,
        f"{PYTHON}-minimal",
        "python3-pip",
        "nginx",
        "libpq-dev",
    ]
    connection.run(f"sudo apt-get install --yes {' '.join(packages)}")


def _get_latest_source(connection):
    if exists(connection, ".git"):
        connection.run("git fetch")
    else:
        connection.run(f"git clone {REPO_URL} .")
    current_commit = run("git log -n 1 --format=%H").stdout
    connection.run(f"git reset --hard {current_commit}")


def _update_virtualenv(connection):
    if not exists(connection, "venv"):
        connection.run(f"{PYTHON} -m virtualenv venv")

    with connection.prefix(". venv/bin/activate"):
        connection.run(f"python -m pip install --upgrade pip")
        connection.run(f"python -m pip install --upgrade poetry")
        connection.run("poetry install")


def _create_or_update_dotenv(connection):
    if not exists(connection, ".env"):
        connection.run("cp .env-deploy .env")

    current_contents = connection.run("cat .env").stdout
    if "SECRET_KEY" not in current_contents:
        new_secret = "".join(
            random.SystemRandom().choices(string.ascii_lowercase + string.digits, k=50)
        )
        append(connection, ".env", f"SECRET_KEY={new_secret}")


def _update_database(connection):
    with connection.prefix(". venv/bin/activate"):
        connection.run("python -m flask db upgrade")
