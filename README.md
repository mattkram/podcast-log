# podcast-log

[![codecov](https://codecov.io/bb/mattkram/podcast-log/branch/develop/graph/badge.svg?token=JhVZChkAR9)](https://codecov.io/bb/mattkram/podcast-log)

A simple Flask application for following and keeping a podcast listen log.

## Getting started

Install with `pipenv`:

```
pipenv install
```

Initialize the database:

```
flask db upgrade
```

Run the test server:

```
FLASK_APP=podcast_log && flask run
```
