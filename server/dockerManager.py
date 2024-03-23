import docker

import os.path as path
from asyncio import sleep as asleep

class DockerManager:

    def __init__(self, logger, name: str, tagname: str, build_context: str) -> None:
        self.logger = logger
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
        raise Exception("Dockerfile not found")

    def stopContainer(self) -> None:
        for container in self.client.containers.list(all=True):
            if container.name == self.name:
                # log stop and remove
                self.logger.info("Stopping container: {container.name}")
                container.stop()
                self.logger.info("Removing container: {container.name}")
                container.remove(v=True, force=True)
                return
        # log error
        self.logger.error(f"Could not find container with name: {self.name}")

    def deleteImage(self) -> None:
        if [f"{self.tagname}:latest"] in [image.tags for image in self.client.images.list()]:
            # log removing tag
            self.logger.info(f"Deleting image: {self.tagname}")
            self.client.images.remove(image=self.tagname)
        else:
            pass # log error

    def buildImage(self) -> None:
        # log building image
        self.logger.info(f"Building new image: {self.tagname}")
        self.client.images.build(path=self.build_context, dockerfile=self.dockerfile, tag=self.tagname)

    def runContainer(self) -> None:
        # log starting container
        self.logger.info(f"Running new image: {self.name} with image {self.tagname}")
        container = self.client.containers.run(self.tagname, name=self.name, detach=True)
        timeout = 30 # timeout in seconds
        period = 5 # how long to wait between checks
        elased_time = 0 # keep track of e
        while container.status != "running" or elased_time < timeout:
            # asleep(period)
            elased_time += period


    def reload(self) -> None:
        self.stopContainer()
        self.deleteImage()
        self.buildImage()
        self.runContainer()

