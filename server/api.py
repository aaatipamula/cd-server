from flask import Blueprint, request, current_app

import os
import traceback
import subprocess as sp
import os.path as path

from server import dockerManager
from server.auth import requires_auth
from server.secret import compare
from server.util import convertForm, findEnvFile, writeEnvContent
from server.models.githubPullRequestPayload import PullRequestPayload
from server.models.githubPushPayload import PushPayload

api = Blueprint("api", __name__, url_prefix="/api")

@api.post('/webhooks')
def push_event():
    DEV_DIRECTORY = current_app.config["DEV_DIRECTORY"]
    SECRET_KEY = current_app.config["SECRET_KEY"]
    DOCKER_RELOAD_SCRIPT = current_app.config["DOCKER_RELOAD_SCRIPT"]

    try:
        if request.json is None:
            return {"error": "No data in request"}, 400

        payload = PushPayload(**request.json) \
            if "after" in request.json else PullRequestPayload(**request.json)
        repo_dir = path.join(DEV_DIRECTORY, payload.repository.name)

        request_signature = request.headers.get('X_HUB_SIGNATURE_256')
        if request_signature is None:
            # Change to raise error
            current_app.logger.error("No X-Hub-Signature-256 signature found")
            return {"error": "Missing request signature."}, 400

        if isinstance(payload, PullRequestPayload) and payload.action != "closed":
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
            # dockerManager.reload(
            #     payload.repository.name.lower(),
            #     payload.repository.full_name.lower(),
            #     repo_dir,
            # )
            reload_proc = sp.run(
                ["/bin/sh", DOCKER_RELOAD_SCRIPT, payload.repository.name.lower()],
                # capture_output=True,
                stdout=sp.PIPE,
                stderr=sp.PIPE,
                check=True
            )
            current_app.logger.info(reload_proc.stdout.decode('utf-8'))
            current_app.logger.error(reload_proc.stderr.decode('utf-8'))

            return {"success": "Image is up and running."}, 201

        else:
            return {"error": "Invalid request."}, 401

    except Exception as err:
        traceback.print_exception(err)
        return {"error": "Something unexpected went wrong."}, 500

@api.post("/env")
@requires_auth(is_api=True)
def post_env():
    DEV_DIRECTORY = current_app.config["DEV_DIRECTORY"]
    
    container_id = request.args.get("id")

    try: 
        if not container_id:
            return {"error": "Missing container id"}, 404
        else:
            container_name = dockerManager.getContainer(container_id).name

        basepath = path.join(DEV_DIRECTORY, container_name)
        path_to_env = findEnvFile(DEV_DIRECTORY, container_name)

        if not path.isdir(basepath):
            print(basepath, "does not exist")
            return {"error": "Project folder does not exist"}, 404

        container_env = convertForm(request.form, container_name)
        writeEnvContent(container_env, path_to_env)

        return {"message": "okay"}, 200
    
    except FileNotFoundError:
        return {"error": "Env file was not found"}, 404

