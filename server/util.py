from os import path
from typing import Dict

from werkzeug.datastructures import ImmutableMultiDict

def envToStr(env: Dict[str, str]) -> str:
    return "\n".join(f"{key}={item}" for key, item in env.items())

def readEnvContent(basepath: str, name: str) -> str:
    env_path = path.join(basepath, name, ".env")
    try:
        with open(env_path) as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return ""

def writeEnvContent(env: Dict[str, str], basepath: str) -> None:
    env_path = path.join(basepath, ".env")
    env_content = envToStr(env)
    with open(env_path, "w") as file:
        file.write(env_content)

def parseEnv(env_content: str) -> Dict[str, str]:
    env = {}
    for var in env_content.splitlines():
        pair = var.split("=")
        if len(pair) == 2:
            key, value = pair
            env[key] = value
    return env

def getEnv(basepath: str, name: str) -> Dict[str, str]:
    file_content = readEnvContent(basepath, name)
    return parseEnv(file_content)

def convertForm(form: ImmutableMultiDict[str, str], name: str) -> Dict[str, str]:
    keys = form.getlist(f"{name}-key")
    values = form.getlist(f"{name}-value")
    return {key: value for key, value in zip(keys, values)}

