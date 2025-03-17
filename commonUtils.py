import numpy as np
import sys
import importlib
import unicodedata
import re

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

def normalize_string(value):
    """
    Normalize a string by removing accents, special characters, and replacing spaces with underscores.

    Args:
        value (str): The input string to be normalized.

    Returns:
        str: A normalized string.
    """
    # Remove accents
    normalized = unicodedata.normalize('NFD', value)
    normalized = normalized.encode('ascii', 'ignore').decode('utf-8')

    # Remove special characters (everything except alphanumerics and underscores)
    normalized = re.sub(r'[^a-zA-Z0-9_]', '_', normalized)

    # Ensure no duplicate underscores
    normalized = re.sub(r'_+', '_', normalized)

    # Strip trailing or leading underscores
    normalized = normalized.strip('_')

    return normalized
