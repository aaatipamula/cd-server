import docker
import os.path as path

class DockerManager:

    def __init__(self, name: str, tagname: str, local_dir: str) -> None:
        self.name = name
        self.tagname = tagname
        self.client = docker.from_env()
        self.dockerfile = self.findDockerfile(local_dir)

    @staticmethod
    def findDockerfile(dir: str) -> str:
        location_one = path.join(dir, "Dockerfile")
        location_two = path.join(dir, "scripts", "Dockerfile") 
        return location_one if path.isfile(location_one) else location_two

    def stopContainer(self) -> None:
        for container in self.client.containers.list():
            if container.name == self.name:
                # log stop and remove
                container.stop()
                container.remove(v=True, force=True)
                return
        # log error

    def deleteImage(self) -> None:
        if f"{self.tagname}:latest" in [image.tags for image in self.client.images.list()]:
            # log removing tag
            self.client.images.remove(image=self.tagname)
        else:
            pass # log error

    def buildImage(self) -> None:
        # log building image
        with open(self.dockerfile) as file:
            self.client.images.build(fileobj=file, tag=self.tagname)

    def runContainer(self) -> None:
        # log starting container
        self.client.containers.run(self.tagname, name=self.name, detach=True)

    def reload(self) -> None:
        self.stopContainer()
        self.deleteImage()
        self.buildImage()
        self.runContainer()

