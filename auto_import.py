import os

'''
auto_import.py checks if modules can be imported on another python file and automatically installs modules that have not been installed.

To use auto_import.py, you must:
1. from auto_import import auto_import
2. exec(auto_import("module name"))

This way, when the user runs the program, all necessary modules will be installed on their own.
'''


def auto_import(module):
    try:
        exec(f"import {module}") # check if module is installed
        return f"import {module}" # if so, module can be imported on the other file
    except ImportError: # if module is not installed
        print(f"Automatically installing {module}...\n")
        try:
            os.system(f'python -m pip install {module}') # try using the pip command (works for some devices)
            print(f"Successfully installed {module}.")
        except ImportError: # if the python command failed
            try:
                os.system(f'python -m pip3 install {module}') # use the pip3 command (works for most devices unless python is not installed)
                print(f"Successfully installed {module}.\n")
            except ImportError:
                print(f"ERROR: Failed to installed {module}.")
        return f"import {module}" # return the command to import the module on the other file
