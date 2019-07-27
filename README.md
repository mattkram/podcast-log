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

## Deploying to AWS Lightsail

[Article 1](https://threenine.co.uk/connect-aws-lightsail-ssh-with-ubuntu-terminal/)

[Article 2](https://nerderati.com/2011/03/17/simplify-your-life-with-an-ssh-config-file/)

1. Download the public key from AWS, move to `~/.ssh/lightsail.pem`
1. Change the permissions: `chmod 0400 ~/.ssh/lightsail.pem`
1. Connect via `ssh -I ~/.ssh/lightsail.pem -T ubuntu@${LIGHTSAIL_IP}`
1. Save settings in `~/.ssh/config`:
    ```
    Host lightsail
        Hostname $LIGHTSAIL_IP
        User ubuntu
        IdentityFile ~/.ssh/lightsail.pem
    ```
1. I can now connect with `ssh lightsail`
