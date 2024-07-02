import fnmatch
import os
from os import path
from typing import Dict

from werkzeug.datastructures import ImmutableMultiDict

def envToStr(env: Dict[str, str]) -> str:
    return "\n".join(f"{key}={item}" for key, item in env.items())

def findEnvFile(basepath: str, name: str) -> str:
    src = path.join(basepath, name)
    for root, _, filenames in os.walk(src):
        for filename in fnmatch.filter(filenames, '.env'):
            return os.path.join(root, filename)
    return path.join(src, ".env")

def readEnvContent(filePath: str) -> str:
    if path.isfile(filePath):
        with open(filePath) as file:
            content = file.read()
            return content
    else:
        return ""

def writeEnvContent(env: Dict[str, str], env_path: str) -> None:
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
    path_to_env = findEnvFile(basepath, name)
    file_content = readEnvContent(path_to_env)
    return parseEnv(file_content)

def convertForm(form: ImmutableMultiDict[str, str], name: str) -> Dict[str, str]:
    keys = form.getlist(f"{name}-key")
    values = form.getlist(f"{name}-value")
    return {key: value for key, value in zip(keys, values)}

