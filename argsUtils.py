import sys

def getConfig(params=[], paramsWithDefaultValue=[], checkParameters=True, checkParametersFunction=None):
    """
    Get configuration data from the command line arguments.

    Returns:
    - dict: Configuration data.
    """
    config = {}

    for i in range(1, len(sys.argv)):
        for param in params:
            if sys.argv[i].startswith(f"{param}="):
                config[param] = sys.argv[i].replace(f"{param}=", "")
    isConfigValid = True
    for param in params:
        if param not in config:
            print(f"Missing parameter {param}")
            if param in paramsWithDefaultValue:
                print("Default value will be applied for this parameter")
            else:
                isConfigValid = False

    if not isConfigValid:
        print(f"List of required parameters : {params}")
        sys.exit(1)
    if checkParametersFunction != None:
        isConfigValid = checkParametersFunction(config)
        if not isConfigValid:
            print(f"Parameters are not valid.")
            sys.exit(1)
    elif checkParameters:
        print("Error : Unable to check parameters.")

    return config