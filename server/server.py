from flask import Flask, request 
from dotenv import load_dotenv

import os
import traceback
import subprocess as sp
import os.path as path

from server.secret import compare
from server.dockerManager import DockerManager
from server.utils.githubPullRequestPayload import Payload

load_dotenv(".env")
app = Flask("cd-server")

app.logger.info("Starting server")

dockerManager = DockerManager(logger=app.logger)

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
        payload = Payload(**request.json) # Known pyright issue
        repo_dir = path.join(DEV_DIRECTORY, payload.repository.name)

        request_signature = request.headers.get('X_HUB_SIGNATURE_256')
        if request_signature is None:
            # Change to raise error
            app.logger.error("No X-Hub-Signature-256 signature found")
            return {"error": "Missing request signature."}, 400

        if payload.action != "closed":
            return {"msg": f"Ignoring action {payload.action}."}, 100

        # Check for valid requests
        if compare(SECRET_KEY, request.get_data(as_text=True), request_signature):

            if not path.isdir(repo_dir):
                app.logger.info("Cloning directory.")
                os.chdir(DEV_DIRECTORY)
                sp.run(['git', 'clone', payload.repository.clone_url])
                os.chdir(repo_dir)
            else:
                app.logger.info(f"Updating {payload.repository.name}")
                os.chdir(repo_dir)
                sp.run(['git', 'pull'])

            app.logger.info(f"Reloading docker image for {payload.repository.name}")
            dockerManager.reload(
                payload.repository.name,
                payload.repository.full_name,
                repo_dir,
            )

            return {"success": "Image is up and running."}, 201

        else:
            # Change to raise error
            return {"error": "Invalid request."}, 401

    except Exception as err:
        traceback.print_exception(err)
        return {"error": "Something unexpected went wrong."}, 500

