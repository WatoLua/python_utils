import logging

logging.basicConfig(
    filename=f'out.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def getLogger(forFilePath, pathSeparator = "\\"):
    logging.basicConfig(
        filename=f'{forFilePath}.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(forFilePath.split(pathSeparator)[-1])