import logging
import sys
import atexit

logging.basicConfig(
    filename=f'out.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

_localLogging = {}

def getDefaultLogger():
    if "default" in _localLogging:
        return _localLogging["default"]

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
    _localLogging["default"] = root
    return root

def getLogger(forFilePath, pathSeparator = "/"):
    print(f"logging in {forFilePath.replace("\\", pathSeparator)}")
    if forFilePath in _localLogging:
        return _localLogging[forFilePath]
    logging.basicConfig(
        filename=f'{forFilePath}.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(forFilePath.replace("\\", pathSeparator))

def closeAllLoggers():
    """Close all loggers and remove all handlers."""
    print("closing all loggers")
    for logger in _localLogging.values():
        for handler in logger.handlers:
            handler.close()
            logger.removeHandler(handler)
    _localLogging.clear()

atexit.register(closeAllLoggers)