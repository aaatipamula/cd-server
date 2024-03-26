import docker


import os.path as path
import logging

class DockerManager:

    def __init__(self, name: str, tagname: str, build_context: str, logger = None) -> None:
        self.logger = logger if logger else logging.getLogger("dockerManager")
        self.logger.setLevel(logging.DEBUG)
        self.name = name
        self.tagname = tagname
        self.build_context = build_context

        self.client = docker.from_env()
        self.dockerfile = self.findDockerfile(build_context)

    @staticmethod
    def findDockerfile(directory: str) -> str:
        location_one = path.join(directory, "Dockerfile")
        location_two = path.join(directory, "scripts", "Dockerfile")
        if path.isfile(location_one): return location_one
        elif path.isfile(location_two): return location_two
        # Raise specific exception type
        raise Exception("Dockerfile not found")

    def stopContainer(self) -> None:
        for container in self.client.containers.list(all=True):
            if container.name == self.name:
                # log stop and remove
                self.logger.debug(f"Stopping container: {container.name}")
                container.stop()
                self.logger.debug(f"Removing container: {container.name}")
                container.remove(v=True, force=True)
                return
        # log error
        self.logger.error(f"Could not find container with name: {self.name}")
        # Raise specific exception type

    def deleteImage(self) -> None:
        if [f"{self.tagname}:latest"] in [image.tags for image in self.client.images.list()]:
            # log removing tag
            self.logger.debug(f"Deleting image: {self.tagname}")
            self.client.images.remove(image=self.tagname)
        else:
            pass # log error and raise specific exception

    def buildImage(self) -> None:
        # log building image
        self.logger.debug(f"Building new image: {self.tagname}")
        self.client.images.build(
            path=self.build_context,
            dockerfile=self.dockerfile,
            tag=self.tagname,
            rm=True
        )

    def runContainer(self) -> None:
        # log starting container
        # TODO: Parse info for volumes etc
        self.logger.debug(f"Running new image: {self.name} with image {self.tagname}")
        self.client.containers.run(self.tagname, name=self.name, detach=True)

    def reload(self) -> None:
        self.stopContainer()
        self.deleteImage()
        self.buildImage()
        self.runContainer()

