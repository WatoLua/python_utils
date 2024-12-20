import numpy as np
import sys
import importlib

## data parsing ##

def np_decode(object):
    if isinstance(object, np.generic):
        return object.item()
    else:
        return object

## args handler ##

# you specify a relative path without .py in your string
def importFunctions(modulePath):
    sys.path.append(modulePath)
    importedFunctions = importlib.import_module(modulePath.split("/")[-1])
    return importedFunctions

# you can use absolute path
def importFunctionsV2(modulePath):
    sys.path.append("/".join(modulePath.split("/")[:-1]))
    importedFunctions = importlib.import_module(modulePath.split("/")[-1][:-3])
    return importedFunctions