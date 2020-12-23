import os
import subprocess
import sys
import argparse


VIRTUALENV_LIB_NAME = 'virtualenv'
TEMP_FOLDER_PATH = r'temp_virtual_env'
REQUIREMENTS_FILE = os.path.join(TEMP_FOLDER_PATH, r'requirements.txt')
VIRTUALENV_PIP = os.path.join(TEMP_FOLDER_PATH, 'Scripts', 'pip')


def create_offline_installer(package_name):
    # Install virtualenv if it's not already installed
    if VIRTUALENV_LIB_NAME not in sys.modules:
        subprocess.check_call([sys.executable, "-m", "pip", "install", VIRTUALENV_LIB_NAME])

    # Install the requested package inside the temporary virtualenv
    subprocess.check_call([sys.executable, "-m", "virtualenv", TEMP_FOLDER_PATH])
    subprocess.check_call([os.path.join(TEMP_FOLDER_PATH, 'Scripts', 'activate.bat')])
    subprocess.check_call([VIRTUALENV_PIP, "install", package_name])

    with open(REQUIREMENTS_FILE, "w") as requirements_file:
        subprocess.check_call([VIRTUALENV_PIP, "freeze"], stdout=requirements_file)

    # Create the offline installation folder
    subprocess.check_call([VIRTUALENV_PIP, "download", "-r", REQUIREMENTS_FILE,
                           "-d", f"offline-{package_name}-installer"])
    # TODO Move the requirements file to this folder

    # TODO Create the installation script for this package


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creating an offline installer for a python package.')
    parser.add_argument('requested_package', help='The name of the requested package')
    args = parser.parse_args()

    create_offline_installer(args.package_name)
