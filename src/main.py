from flask import Flask, request
from os import chdir
import docker
import subprocess as sp
import os.path as path

app = Flask("cd-server")
docker_client = docker.from_env()

DEV_DIRECTORY="/home/aaatipamula/projects"
SQL_DB="/path/to/sql/db"

@app.route('/webhooks', methods=["POST"])
def push_event():
    if request.method == "POST":
        repo: str = request.json["repository"]["name"]
        repoDir: str = path.join(DEV_DIRECTORY, repo)

        chdir(repoDir)
        sp.run(['git', 'pull', 'origin', 'master'])

        # if valid_repo():

        for container in docker_client.containers.list():
            if container.name == repo:
                container.remove(force=True)

        if f"{repo}:latest" in [image.tags for image in docker_client.images.list()]:
            docker_client.images.remove(image=repo)

        docker_client.build(path="./scripts", tag=repo)
        docker_client.run(repo, name=repo, detach=True)
