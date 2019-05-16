import sys
import platform
import importlib

from general import run_command

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

def install_packages(requirements_file):
    """ Installs all packages specified in Requirements.txt file """
    run_command('pip install -r {}'.format(requirements_file))

def verify_installed_packages(requirements_file):
    """
    Verify if packages specified in Requirements.txt is installed
    """
    # Get the required packages from Requirements.txt file
    with open(requirements_file, 'r') as req_file:
        packages_versions = req_file.readlines()
        package_names = [package.split('=')[0].strip() for package in packages_versions]
    
    # Try to import every package, report if installed or not
    for package_name in package_names:
        print(package_name)
        try:
            importlib.import_module(package_name, package=None)
        except ImportError:
            print('{} is not installed'.format(package_name))
        else:
            print('{} is installed'.format(package_name))