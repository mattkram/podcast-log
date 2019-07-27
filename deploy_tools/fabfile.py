import os
import random
import string
from tempfile import TemporaryFile

import jinja2
from dotenv import load_dotenv
from invoke import run, task
from patchwork.files import append, exists, contains

load_dotenv()

REPO_URL = os.environ["REPO_URL"]
PYTHON = "python3.7"
template_loader = jinja2.FileSystemLoader(searchpath="./deploy_tools/")
template_env = jinja2.Environment(loader=template_loader)


@task
def init_server(c):
    _update_system_dependencies(c)


@task
def deploy(c):
    site_folder = f"/home/{c.user}/sites/{c.host}"
    c.run(f"mkdir -p {site_folder}")
    with c.cd(site_folder):
        _get_latest_source(c)
        _update_virtualenv(c)
        _create_or_update_dotenv(c)
        _update_database(c)
        _prepare_nginx_config(c)
        _prepare_gunicorn_config(c)


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

    if not contains(connection, ".env", "SECRET_KEY"):
        new_secret = "".join(
            random.SystemRandom().choices(string.ascii_lowercase + string.digits, k=50)
        )
        append(connection, ".env", f"SECRET_KEY={new_secret}")


def _update_database(connection):
    with connection.prefix(". venv/bin/activate"):
        connection.run("python -m flask db upgrade")


def _prepare_nginx_config(connection):
    template = template_env.get_template("nginx_template")
    output_text = template.render(
        application_name="podcast_log", hostname=connection.host
    )
    filename = f"nginx-{connection.host}"
    with TemporaryFile(mode="r+") as fp:
        fp.write(output_text)
        connection.put(fp, f"{connection.cwd}/{filename}")
    connection.run(f"sudo mv {filename} /etc/nginx/sites-available/{connection.host}")

    connection.run(
        " ".join(
            [
                "sudo ln -fs",
                f"/etc/nginx/sites-available/{connection.host}",
                f"/etc/nginx/sites-enabled/{connection.host}",
            ]
        )
    )
    connection.run(f"sudo systemctl start nginx")
    connection.run(f"sudo systemctl reload nginx")


def _prepare_gunicorn_config(connection):
    template = template_env.get_template("gunicorn_template.service")
    output_text = template.render(
        application_name="podcast_log",
        username=connection.user,
        hostname=connection.host,
        deploy_dir=connection.cwd,
    )
    service_name = f"gunicorn-{connection.host}-podcast_log"
    filename = f"{service_name}.service"
    with TemporaryFile(mode="r+") as fp:
        fp.write(output_text)
        connection.put(fp, f"{connection.cwd}/{filename}")
    connection.run(f"sudo mv {filename} /etc/systemd/system")
    connection.run("sudo systemctl daemon-reload")
    connection.run(f"sudo systemctl enable {service_name}")
    connection.run(f"sudo systemctl start {service_name}")
    connection.run(f"sudo systemctl reload-or-restart {service_name}")
