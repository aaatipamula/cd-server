from flask import Flask, request 
from dotenv import load_dotenv

import logging
import os
import subprocess as sp
import os.path as path

from server.secret import compare
from server.utils.githubPullRequestPayload import Payload

load_dotenv(".env")
app = Flask("cd-server")

DEV_DIRECTORY = os.environ.get("FLASK_DEV_FOLDER", "")
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "")

# Check env
if not(DEV_DIRECTORY or SECRET_KEY):
    raise RuntimeError("Missing required environment variables")


@app.post('/webhooks')
def push_event():

    # Define repo and associated directory
    # TODO: Sanitize repo name
    payload = Payload(**request.json)
    tagname = payload.repository.full_name
    repo_dir = path.join(DEV_DIRECTORY, payload.repository.name)

    # TODO: create function to find Dockerfile
    script_dir = path.join(repo_dir, "scripts")

    request_signature = request.headers.get('X_HUB_SIGNATURE_256')
    if not request_signature:
        return {"error": "Missing request signature"}, 400

    # Check for valid requests
    if compare(SECRET_KEY, request.get_data(as_text=True), request_signature):

        if not path.isdir(repo_dir):
            os.chdir(DEV_DIRECTORY)
            logging.debug(f"Cloning {payload.repository.name} into {repo_dir}")
            sp.run(['git', 'clone', payload.repository.clone_url])
            os.chdir(repo_dir)
        else:
            os.chdir(repo_dir)
            logging.debug(f"Updating {payload.repository.name} from master")
            sp.run(['git', 'pull', 'origin', 'master'])

        if not path.isdir(script_dir):
            return {"error": "Scripts directory does not exist"}, 404


        return {"success": "Image is up and running."}, 200

    else:
        return {"error": "Not a valid request."}, 400

