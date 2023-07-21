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
# Running

## Devlopment

```
python3 -m flask --app src/main.py run
```
