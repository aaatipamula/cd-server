import docker
from docker.errors import DockerException

import os.path as path
import logging

class DockerManager:

    def __init__(self, logger = None) -> None:
        self.logger = logger if logger else logging.getLogger("dockerManager")
        self.logger.setLevel(logging.DEBUG)

        self.client = docker.from_env()

    @staticmethod
    def findDockerfile(directory: str) -> str:
        location_one = path.join(directory, "Dockerfile")
        location_two = path.join(directory, "scripts", "Dockerfile")
        if path.isfile(location_one): return location_one
        elif path.isfile(location_two): return location_two
        # Raise specific exception type
        raise DockerException("Dockerfile not found")

    def stopContainer(self, name: str) -> None:
        for container in self.client.containers.list(all=True):
            if container.name == name:
                # log stop and remove
                self.logger.debug("Stopping container: %s", container.name)
                container.stop()
                self.logger.debug("Removing container: %s", container.name)
                container.remove(v=True, force=True)
                return
        # log error
        self.logger.error("Could not find container with name: %s", name)
        raise DockerException(f"Could not find container with name: {name}")

    def deleteImage(self, tagname: str) -> None:
        if [f"{tagname}:latest"] in [image.tags for image in self.client.images.list()]:
            # log removing tag
            self.logger.debug("Deleting image: %s", tagname)
            self.client.images.remove(image=tagname)
        else:
            self.logger.error("Image with %s not found", tagname)
            raise DockerException(f"Image with {tagname} not found")

    def buildImage(self, tagname: str, build_context: str, dockerfile: str) -> None:
        # log building image
        self.logger.debug("Building new image: %s", tagname)
        self.client.images.build(
            path=build_context,
            dockerfile=dockerfile,
            tag=tagname,
            rm=True
        )
        # Maybe add a check for successful image build

    def runContainer(self, name: str, tagname: str) -> None:
        # log starting container
        # TODO: Parse info for volumes etc
        self.logger.debug("Running new image: %s with image %s", name, tagname)
        self.client.containers.run(tagname, name=name, detach=True)
        # Try and add check for running container

    def reload(self, name: str, tagname: str, build_context: str,) -> None:
        dockerfile = self.findDockerfile(build_context)

        self.stopContainer(name)
        self.deleteImage(tagname)
        self.buildImage(tagname, build_context, dockerfile)
        self.runContainer(name, tagname)

