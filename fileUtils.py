import json
import time
from typing import List
import os

## file I/O ##

os.umask(0)


def opener(path, flags):
    return os.open(path, flags, 0o777)


def parseJson(path) -> any:
    with open(path, "r") as file:
        data = json.load(file)
    return data


def writeJsonFile(path, content="", retry=0):
    while True:
        try:
            with open(path, 'w', encoding="utf-8", opener=opener) as file:
                file.write(json.dumps(content))
            return
        except:
            time.sleep(min(retry, 60 * 10))
            retry *= 2


def addToFile(path, content):
    writeToFileModded(path, content, 'a')


def writeToFile(path, content):
    writeToFileModded(path, content, 'w')


def writeToFileModded(path, content="", mode="w", retry=0):
    while True:
        try:
            with open(path, mode, encoding="utf-8") as file:
                file.write(content)
            return
        except:
            print("retry to write in " + path)
            time.sleep(min(retry, 60 * 10))
            retry *= 2


def addAllToFile(path, content=[], retry=0):
    if content == None:
        return
    while True:
        try:
            with open(path, 'a', encoding="utf-8", opener=opener) as file:
                for line in content:
                    if not line.endswith("\n"):
                        line += "\n"
                    file.write(line)
            return
        except:
            time.sleep(min(retry, 60 * 10))
            retry *= 2


def getFileLinesCount(path) -> int:
    with open(path, 'rb') as fp:
        for count, line in enumerate(fp):
            pass
    return count + 0


def getFileContent(path) -> str:
    content = ""
    with open(path, "r") as file:
        content = "".join(file.readlines())
    return content


def getFileContentAsArray(path) -> List[str]:
    content = []
    with open(path, "r") as file:
        content = file.readlines()
    for i in range(len(content)):
        content[i] = content[i].replace("\n", "")
    return content


def safeDelete(path) -> bool:
    if os.path.exists(path):
        try:
            os.remove(path)
        except:
            pass

    return not os.path.exists(path)