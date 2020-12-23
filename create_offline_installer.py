import importlib.util
import os
import subprocess
import sys
import argparse


VIRTUALENV_LIB_NAME = 'virtualenv'
TEMP_FOLDER_PATH = r'temp_virtual_env'
REQUIREMENTS_FILE_NAME = r'requirements.txt'
TEMP_REQUIREMENTS_FILE = os.path.join(TEMP_FOLDER_PATH, REQUIREMENTS_FILE_NAME)
VIRTUALENV_PIP = os.path.join(TEMP_FOLDER_PATH, 'Scripts', 'pip')
OUTPUT_FOLDER_NAME = "offline-{}-installer"
INSTALLATION_SCRIPT_PATH = os.path.join(OUTPUT_FOLDER_NAME, r'install.py')
OFFLINE_INSTALLATION_COMMAND = 'import subprocess\nimport sys\nsubprocess.check_call([sys.executable, "-m", "pip", ' \
                              '"install", "--no-index", "--find-links=./", "-r", "requirements.txt"]) '


def create_offline_installer(package_name):
    # Install virtualenv if it's not already installed
    if VIRTUALENV_LIB_NAME not in sys.modules and importlib.util.find_spec(VIRTUALENV_LIB_NAME) is None:
        subprocess.check_call([sys.executable, "-m", "pip", "install", VIRTUALENV_LIB_NAME])

    # Install the requested package inside the temporary virtualenv
    subprocess.check_call([sys.executable, "-m", "virtualenv", TEMP_FOLDER_PATH])
    subprocess.check_call([os.path.join(TEMP_FOLDER_PATH, 'Scripts', 'activate.bat')])
    subprocess.check_call([VIRTUALENV_PIP, "install", package_name])

    with open(TEMP_REQUIREMENTS_FILE, "w") as requirements_file:
        subprocess.check_call([VIRTUALENV_PIP, "freeze"], stdout=requirements_file)

    # Create the offline installation folder
    subprocess.check_call([VIRTUALENV_PIP, "download", "-r", TEMP_REQUIREMENTS_FILE,
                           "-d", OUTPUT_FOLDER_NAME.format(package_name)])
    # Move the requirements file to this folder
    os.replace(TEMP_REQUIREMENTS_FILE, os.path.join(OUTPUT_FOLDER_NAME.format(package_name), REQUIREMENTS_FILE_NAME))

    # Create the offline installation script for this package
    with open(INSTALLATION_SCRIPT_PATH.format(package_name), 'w') as script_file:
        script_file.write(OFFLINE_INSTALLATION_COMMAND)

    # TODO Remove the temporary folder


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creating an offline installer for a python package.')
    parser.add_argument('requested_package', help='The name of the requested package')
    args = parser.parse_args()

    create_offline_installer(args.requested_package)
