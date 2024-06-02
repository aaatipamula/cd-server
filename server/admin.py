from flask import Blueprint, current_app, render_template, request

from server import dockerManager
from server.util import getEnv
from server.auth import requires_auth

admin = Blueprint("admin", __name__, url_prefix="/admin")

@admin.get("/")
@requires_auth()
def get_admin():
    DEV_DIRECTORY = current_app.config["DEV_DIRECTORY"]

    containers = [
        {
            "id": container.id,
            "name": container.name,
            "image": ", ".join(container.image.tags),
            "status": container.status,
            "logs": container.logs(tail=200).decode('utf-8'),
            "env": getEnv(DEV_DIRECTORY, container.name)
        }
        for container in dockerManager.containers
    ]
    active_container = request.args.get("active", containers[0]["name"])

    return render_template("admin.html", containers=containers, active=active_container)
    
