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

def cycle_from_to(from_, to):
    n = from_
    while True:
        yield n
        n = (n + 1) % to

def deep_getsizeof(obj, seen=None):
    """Approximate memory footprint of an object and its contents."""
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)

    size = sys.getsizeof(obj)

    if isinstance(obj, dict):
        size += sum(
            deep_getsizeof(k, seen) + deep_getsizeof(v, seen)
            for k, v in obj.items()
        )
    elif isinstance(obj, (list, tuple, set, frozenset)):
        size += sum(deep_getsizeof(i, seen) for i in obj)

    return size

def print_sizeof(data=None, sizeof=None):
    if data is None and sizeof is None:
        print("You must provide either data or sizeof.")

    if data is not None:
        sizeof_ = deep_getsizeof(data)
        print_sizeof(sizeof=sizeof_)

    if sizeof is not None:
        print(sizeof * 8, "b")
        print(sizeof, "B")
        print(round(sizeof / 1024, 2), "KiB")
        print(round(sizeof / 1024 ** 2, 2), "MiB")
        print(round(sizeof / 1024 ** 3, 2), "GiB")