import logging

logging.basicConfig(
    filename=f'out.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def getLogger(forFilePath, pathSeparator = "/"):
    print(f"logging in {forFilePath.replace("\\", pathSeparator)}") 
    logging.basicConfig(
        filename=f'{forFilePath}.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(forFilePath.replace("\\", pathSeparator))