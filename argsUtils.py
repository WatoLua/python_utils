import sys

def getConfig(params=[], paramsWithDefaultValue=[], checkParametersFunction=None):
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
            print(f"Error : missing parameter {param}")
            if param in paramsWithDefaultValue:
                print("Default value will be applied for this parameter")
            else:
                isConfigValid = False
    if len(paramsWithDefaultValue) > 1:
        if checkParametersFunction != None:
            checkParametersFunction(config)
        else:
            print("Error : Unable to check parameters")

    if isConfigValid:
        return config
    else:
        print(f"List of required parameters : {params}")
        sys.exit(1)