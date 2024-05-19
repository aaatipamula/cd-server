from os import path
from typing import Dict

from flask import Blueprint, current_app, render_template, request

from server import dockerManager

admin = Blueprint("admin", __name__, url_prefix="/admin")

def getEnvContent(basepath: str, name: str) -> str:
    env_path = path.join(basepath, name, ".env")
    print(env_path)
    try:
        with open(env_path) as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return ""

def parseEnv(env_content: str) -> Dict[str, str]:
    env = {}

    for var in env_content.splitlines():
        pair = var.split("=")
        if len(pair) == 2:
            key, value = pair
            env[key] = value

    return env

def getEnv(basepath: str, name: str) -> Dict[str, str]:
    file_content = getEnvContent(basepath, name)
    return parseEnv(file_content)

@admin.get("/")
def get_admin():
    containers = [
        {
            "id": container.id,
            "name": container.name,
            "image": ", ".join(container.image.tags),
            "status": container.status,
            "logs": container.logs(tail=30).decode('utf-8'),
            "env": getEnv(current_app.config["DEV_FOLDER"], container.name)
        }
        for container in dockerManager.containers
    ]
    return render_template("admin.html", containers=containers)
    
