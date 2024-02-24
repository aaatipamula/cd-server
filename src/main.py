from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, request 
from dotenv import load_dotenv
import docker

import logging
import os
import subprocess as sp
import os.path as path

from secret_key import compare

load_dotenv(".env")

app = Flask("cd-server")
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

dockerClient = docker.from_env()

DEV_DIRECTORY = os.environ.get("FLASK_DEV_FOLDER")
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")

# Check env
if not DEV_DIRECTORY or not SECRET_KEY:
    raise RuntimeError("Missing required environment variables")


@app.post('/webhooks')
def push_event():

    # Define repo and associated directory
    # TODO: Sanitize repo name
    repo = request.json["repository"]["name"]
    tagname = "aaatipamula/" + repo
    repoDir = path.join(DEV_DIRECTORY, repo)
    scriptDir = path.join(repoDir, "scripts")

    request_signature = request.headers.get('X_HUB_SIGNATURE_256')
    if not request_signature:
        return {"error": "Missing request signature"}, 400

    # Check for valid requests
    if compare(SECRET_KEY, request.get_data(as_text=True), request_signature):

        if not path.isdir(repoDir):
            os.chdir(DEV_DIRECTORY)
            logging.debug(f"Cloning {repo} into {repoDir}")
            sp.run(['git', 'clone', f'https://github.com/{tagname}'])
            os.chdir(repoDir)
        else:
            os.chdir(repoDir)
            logging.debug(f"Updating {repo} from master")
            sp.run(['git', 'pull', 'origin', 'master'])

        if not path.isdir(scriptDir):
            return {"error": "Scripts directory does not exist"}, 404

        for container in dockerClient.containers.list():
            if container.name == repo:
                logging.info(f"Stopping container {container.name}")
                container.stop()
                logging.info(f"Removing container {container.name}")
                container.remove(force=True)

        if f"{tagname}:latest" in [image.tags for image in dockerClient.images.list()]:
            logging.info("Removing image {tagname}")
            dockerClient.images.remove(image=tagname)
        else:
            logging.error(f"Image {tagname}:latest not found.")

        logging.info(f"Building image {tagname}")
        dockerClient.images.build(path=scriptDir, tag=tagname)
        logging.info(f"Starting container {repo}")
        dockerClient.containers.run(tagname, name=repo, detach=True)

        return {"success": "Image is up and running."}, 200

    else:
        return {"error": "Not a valid request."}, 400

