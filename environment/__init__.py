import sys
import platform

def __venv_path():
    """
    Return the path of virtual environment of the project \ script
    """
    return sys.executable

def __python_version():
    """
    returns the python version sepcified to the project
    """
    return platform.python_version()

def get():
    """
    Returns environment parameters as a dictionary
    1. Virtual environment path
    2. Python version
    """
    environment = {}
    environment['venv'] = __venv_path()
    environment['python_version'] = __python_version()

    return environment
