import sys

utilsVars = {
    # print var
    "progressBar": -1,
    "progressPourcent": -1
    # ...
}

## print ##

def printProgressBar(actualProgress, maxValue, sizeBar):
    """
    Print a progress bar
    """

    progress = int(actualProgress * 100 / maxValue)

    if utilsVars["progressBar"] != progress:
        utilsVars["progressBar"] = progress
        progress = int(actualProgress * sizeBar / maxValue)
        sys.stdout.write("\r [" + ("#" * progress) + ("-" * (sizeBar - progress)) + "]")
        # sys.stdout.write(f"{actualProgress}/{maxValue}\n")
        sys.stdout.flush()

    if utilsVars["progressBar"] == 100:
        utilsVars["progressBar"] = -1


def printProgress(actualProgress, maxValue, sizeBar):
    """
    Print a progress with values
    """

    progress = int(actualProgress * 100 / maxValue)

    if utilsVars["progressPourcent"] != progress:
        utilsVars["progressPourcent"] = progress
        progress = int(actualProgress * sizeBar / maxValue)
        sys.stdout.write(f"{actualProgress}/{maxValue}\n")
        sys.stdout.flush()

    if utilsVars["progressPourcent"] == 100:
        utilsVars["progressPourcent"] = -1