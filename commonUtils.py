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

def importFunctions(modulePath):
    sys.path.append(modulePath)
    importedFunctions = importlib.import_module(modulePath.split("/")[-1])
    return importedFunctions
