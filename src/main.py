from flask import Flask, request 
from secret_key import compare
from dotenv import load_dotenv
import logging
import os
import docker
import subprocess as sp
import os.path as path

load_dotenv(".env")

app = Flask("cd-server")
dockerClient = docker.from_env()

DEV_DIRECTORY = os.environ.get("DEV_FOLDER")
SECRET_KEY = os.environ.get("SECRET_KEY")

# Check env
if not DEV_DIRECTORY or not SECRET_KEY:
    raise RuntimeError("Missing required environment variables")


@app.post('/webhooks')
def push_event():

    # Define repo and associated directory
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
            sp.run(['git', 'clone', f'https://github.com/aaatipamula/{repo}'])
            os.chdir(repoDir)
        else:
            os.chdir(repoDir)
            logging.debug(f"Updating {repo} from master")
            sp.run(['git', 'pull', 'origin', 'master'])

        if not path.isdir(scriptDir):
            return {"error": "Scripts directory does not exist"}, 404

        for container in dockerClient.containers.list():
            if container.name == repo:
                logging.debug("Stopping container {container.name}")
                container.stop()
                logging.info(f"Removing container {container.name}")
                container.remove(force=True)

        if f"{tagname}:latest" in [image.tags for image in dockerClient.images.list()]:
            logging.info("Removing image {tagname}")
            dockerClient.images.remove(image=tagname)

        logging.info("Building image {tagname}")
        dockerClient.images.build(path=path.join(repoDir, "scripts"), tag=tagname)
        logging.info("Starting container {repo}")
        dockerClient.containers.run(tagname, name=repo, detach=True)

        return {"success": "Image is up and running."}, 200

    else:
        return {"error": "Not a valid request."}, 400

