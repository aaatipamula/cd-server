import docker

client = docker.from_env()

def stopContainer(name: str) -> bool:
    for container in client.containers.list():
        if container.name == name:
            container.stop()
            container.remove(v=True, force=True)
    logging.error(f"Container {name} not found.")

def deleteImage(tagname: str) -> None:
    if f"{tagname}:latest" in [image.tags for image in client.images.list()]:
        logging.info("Removing image {tagname}")
        client.images.remove(image=tagname)
    else:
        logging.error(f"Image {tagname}:latest not found.")

def buildImage(tagname: str, script_dir: str) -> None:
    logging.info(f"Building image {tagname} from path {script_dir}")
    client.images.build(path=script_dir, tag=tagname)

def runContainer(tagname: str, name: str) -> None:
    logging.info(f"Starting container {name}")
    client.containers.run(tagname, name=name, detach=True)

