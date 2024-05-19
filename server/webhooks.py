from flask import Blueprint, request, current_app

import os
import traceback
import subprocess as sp
import os.path as path

from server import dockerManager
from server.secret import compare
from server.utils.githubPullRequestPayload import Payload

webhooks = Blueprint("webhooks", __name__)

@webhooks.post('/webhooks')
def push_event():
    DEV_DIRECTORY = current_app.config["DEV_DIRECTORY"]
    SECRET_KEY = current_app.config["SECRET_KEY"]


    try:
        payload = Payload(**request.json) # Known pyright issue
        repo_dir = path.join(DEV_DIRECTORY, payload.repository.name)

        request_signature = request.headers.get('X_HUB_SIGNATURE_256')
        if request_signature is None:
            # Change to raise error
            current_app.logger.error("No X-Hub-Signature-256 signature found")
            return {"error": "Missing request signature."}, 400

        if payload.action != "closed":
            return {"msg": f"Ignoring action {payload.action}."}, 100

        # Check for valid requests
        if compare(SECRET_KEY, request.get_data(as_text=True), request_signature):

            if not path.isdir(repo_dir):
                current_app.logger.info("Cloning directory.")
                os.chdir(DEV_DIRECTORY)
                sp.run(['git', 'clone', payload.repository.clone_url])
                os.chdir(repo_dir)
            else:
                current_app.logger.info(f"Updating {payload.repository.name}")
                os.chdir(repo_dir)
                sp.run(['git', 'pull'])

            current_app.logger.info(f"Reloading docker image for {payload.repository.name}")
            dockerManager.reload(
                payload.repository.name.lower(),
                payload.repository.full_name.lower(),
                repo_dir,
            )

            return {"success": "Image is up and running."}, 201

        else:
            # Change to raise error
            return {"error": "Invalid request."}, 401

    except Exception as err:
        traceback.print_exception(err)
        return {"error": "Something unexpected went wrong."}, 500
    
