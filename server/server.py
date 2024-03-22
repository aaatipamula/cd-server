from flask import Flask, request 
from dotenv import load_dotenv

import logging
import os
import subprocess as sp
import os.path as path

from server.secret import compare
from server.dockerManager import DockerManager
from server.utils.githubPullRequestPayload import Payload

load_dotenv(".env")
app = Flask("cd-server")

DEV_DIRECTORY = os.environ.get("FLASK_DEV_FOLDER", "")
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "")

# Check env
if not DEV_DIRECTORY or not SECRET_KEY:
    raise RuntimeError("Missing required environment variables")

if not path.isdir(DEV_DIRECTORY):
    os.mkdir(DEV_DIRECTORY)


@app.post('/webhooks')
def push_event():

    try:
        payload = Payload(**request.json)

        repo_dir = path.join(DEV_DIRECTORY, payload.repository.name)
        dockerManager = DockerManager(payload.repository.name, payload.repository.full_name, repo_dir)

        request_signature = request.headers.get('X_HUB_SIGNATURE_256')
        if request_signature is None:
            # Change to raise error
            return {"error": "Missing request signature."}, 400

        # Check for valid requests
        if compare(SECRET_KEY, request.get_data(as_text=True), request_signature):

            if not path.isdir(repo_dir):
                os.chdir(DEV_DIRECTORY)
                sp.run(['git', 'clone', payload.repository.clone_url])
                os.chdir(repo_dir)
            else:
                os.chdir(repo_dir)
                sp.run(['git', 'pull', 'origin', 'master'])

            dockerManager.reload()
            return {"success": "Image is up and running."}, 200

        else:
            # Change to raise error
            return {"error": "Invalid request."}, 400

    except Exception as err:
        return {"error": str(err)}, 400
