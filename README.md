![docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)

# About

> A Flask app that automatically reloads my docker containers

This project arose from the need and want to manage some of my other projects. I like to self host my discord bots to save some money on cloud compute costs. I came up with a lit of other problems I wanted to solve as well.

1. I want my projects to automatically update when I push new code
2. Changing and reloading my project can be done without direct access to my server
3. My app should be secure
4. Deploying the project itself shouldn't be too much of a hassle



# Setup

## Environment Variables

> Should be located in `.env`

> [!NOTE]
> This file can also be automatically generated by the setup script

```sh
FLASK_DEV_FOLDER # Path to directory to host files
FLASK_SECRET_KEY # Key to verify, use src/secret_key.py to generate
FLASK_AUTH_USERNAME # Admin Username
FLASK_AUTH_PASSWORD # Admin Password
FLASK_DOCKER_RELOAD_SCRIPT # Location to docker reload script
```
## Production

### No Service (Not Recommended)

1. Setup `venv`

```sh
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

```sh
pip install -r requirements.txt
```

3. Install Gunicorn

```sh
pip install gunicorn
```

4. Start Gunicorn in the background

```sh
nohup gunicorn -w 4 'server.main:app' > gunicorn.log 2>&1 &
```

### With Service

```sh
./scripts/createsocket.sh <username> <server-ip-domain>
source .venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

# Development Server

## Start Server

```sh
python3 -m flask --app server --debug run
```

## Forward Github Webhooks

```sh
nohup gh webhook forward --repo=aaatipamula/REPOSITORY-NAME --events=pull_request --url=http://localhost:5000/webhooks &
```

