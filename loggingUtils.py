import logging
import sys

logging.basicConfig(
    filename=f'out.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def getDefaultLogger():
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
    return root

def getLogger(forFilePath, pathSeparator = "/"):
    print(f"logging in {forFilePath.replace("\\", pathSeparator)}")
    logging.basicConfig(
        filename=f'{forFilePath}.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(forFilePath.replace("\\", pathSeparator))