from flask import Flask, request 
from secret_key import compare
import os
import setup
import docker
import subprocess as sp
import os.path as path

app = Flask("cd-server")
docker_client = docker.from_env()

DEV_DIRECTORY = app.config.get("DEVFOLDER")
SECRET_KEY = app.config.get("SECRET_KEY")

@app.route('/webhooks', methods=["POST"])
def push_event():

    # Define repo and 
    repo: str = request.json["repository"]["name"]
    repoDir: str = path.join(DEV_DIRECTORY, repo)

    # Define secret keys and server key
    serverKey = request.headers.get('HTTP_X_HUB_SIGNATURE_256')
    secretKeyb = bytes(SECRET_KEY, 'utf-8')

    # Check for valid requests
    if compare(secretKeyb, request.get_data(as_text=True), serverKey):

        if not os.path.isdir(repoDir):
            os.chdir(DEV_DIRECTORY)
            sp.run(['git', 'clone', f'https://github.com/aaatipamula/{repo}.git'])
        else:
            os.chdir(repoDir)
            sp.run(['git', 'pull', 'origin', 'master'])

        for container in docker_client.containers.list():
            if container.name == repo:
                container.remove(force=True)

        if f"{repo}:latest" in [image.tags for image in docker_client.images.list()]:
            docker_client.images.remove(image=repo)

        docker_client.build(path=path.join(repoDir, "scripts"), tag=repo)
        docker_client.run(repo, name=repo, detach=True)

    else:
        return {"error": "Not a valid request."}, 404

if __name__ == "__main__":
    setup.main()
    app.run()
