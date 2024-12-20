from jsonpath_ng.ext import parse

## json ##

def browseJsonPath(jsonObject, path, index=0):
    if path != None and path != "":
        path = path.split(".")
        while not (index >= len(path) or index < 0 or (type(jsonObject) not in [type({}), type([])])):
            if "[" in path[index] and path[index].endswith("]"):
                splitedSubArrayPath = path[index].split("[")
                jsonKey = splitedSubArrayPath[0]
                jsonArrayIndex = int(splitedSubArrayPath[1].replace("]", ""))
                if jsonKey in jsonObject:
                    jsonObject = jsonObject[jsonKey][jsonArrayIndex]
                    index += 1
                else:
                    jsonObject = jsonObject[jsonArrayIndex]
                    index += 1
            else:
                jsonObject = jsonObject[path[index]]
                index += 1
    return jsonObject


def getJsonValueOrDefault(jsonObject, path, defaultValue):
    try:
        value = browseJsonPath(jsonObject, path)
        return value if value != None else defaultValue
    except Exception as error:
        # print(error)
        return defaultValue

def getJsonValue(jsonObject, path):
    return parse(path).find(jsonObject)[0].value

def getJsonValues(jsonObject, path):
    return [match.value for match in parse(path).find(jsonObject)]