# Setup

## Environment Variables

```sh
FLASK_DEV_FOLDER # Path to directory to host files
FLASK_SECRET_KEY # Key to verify, use src/secret_key.py to generate
FLASK_AUTH_USERNAME # Admin Username
FLASK_AUTH_PASSWORD # Admin Password
```
## Host Locally

Setup `venv`

```sh
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies

```sh
pip install -r requirements.txt
```

Install Gunicorn

```sh
pip install gunicorn
```

Start Gunicorn in the background

```sh
nohup gunicorn -w 4 'server.main:app' > gunicorn.log 2>&1 &
```

Or create a service

```sh
./scripts/createsocket.sh YOUR-USERNAME
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
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
