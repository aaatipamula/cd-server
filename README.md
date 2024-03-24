# Setup

## Environment Variables

```sh
DEV_FOLDER # Path to directory to host files
SECRET_KEY # Key to verify, use src/secret_key.py to generate
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
pip install gunicorn
```

Start Gunicorn

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
python3 -m flask --app server.server run
```

## Forward Github Webhooks

```sh
nohup gh webhook forward --repo=aaatipamula/REPOSITORY-NAME --events=pull_request --url=http://localhost:5000/webhooks &
```
