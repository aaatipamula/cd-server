# Setup

## Environment Variables

```sh
DEV_FOLDER # Path to directory to host files
SECRET_KEY # Key to verify, use src/secret_key.py to generate
```
## Forward Github Webhooks

```sh
nohup gh webhook forward --repo=aaatipamula/reponame --events=push --url=http://localhost:5000/webhooks &
```
## Host Locally

Setup `venv`

```sh
python3 -m venv .venv
source .venv/bin/activate
```

Install Dependencies

```sh
pip install -r requirements.txt
pip install gunicorn
```

Start Gunicorn

```sh
nohup gunicorn -w 4 'src/main:app' > gunicorn.log 2>&1 &
```

or create a service

```sh
./scripts/createsocket.sh <username>
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```

# Running

## Devlopment

```sh
python3 -m flask --app src/main.py run
```
