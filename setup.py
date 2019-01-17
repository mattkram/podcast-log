#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shutil
import subprocess
import sys
from pathlib import Path

from setuptools import setup, find_packages, Command

here = Path(__file__).parent

with (here / "README.md").open(encoding="utf-8") as fp:
    long_description = fp.read()

about = {}

with (here / "src" / "podcast_log" / "__version__.py").open() as fp:
    exec(fp.read(), about)

version = about["__version__"]

requirements = ["django", "django_tables2", "feedparser"]
test_requirements = ["pytest", "pytest-cov"]


class UploadCommand(Command):
    """Support setup.py publish."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            shutil.rmtree(here / "dist")
        except FileNotFoundError:
            pass
        self.status("Building Source distribution…")
        subprocess.call([sys.executable, "setup.py", "sdist", "bdist_wheel"])
        self.status("Uploading the package to PyPI via Twine…")
        subprocess.call(["twine", "upload", "dist/*"])
        self.status("Pushing git tags…")
        subprocess.call(["git", "tag", f"v{version}"])
        subprocess.call(["git", "push", "--tags"])
        sys.exit()


setup(
    name="podcast-log",
    version=version,
    description="A simple Django application for following and keeping a podcast listen log.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Matt Kramer",
    author_email="matthew.robert.kramer@gmail.com",
    url="https://bitbucket.org/mattkram/podcast-log",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    tests_require=test_requirements,
    # entry_points={"console_scripts": ["podcast-log=podcast_log.cli:cli"]},
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    cmdclass={"upload": UploadCommand},
)
