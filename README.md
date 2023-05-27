# podcast-log

[![codecov](https://codecov.io/gh/mattkram/podcast-log/branch/main/graph/badge.svg?token=RX6JYUA45F)
](https://codecov.io/gh/mattkram/podcast-log)

A simple Flask application for following and keeping a podcast listen log.

## Getting started

Install with `poetry`:

```
poetry install
```

Initialize the database:

```
flask --app podcast_log db upgrade
```

Run the test server:

```
flask --app podcast_log run
```
