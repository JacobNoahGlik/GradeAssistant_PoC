import subprocess
import importlib
import sys
import os
from presets import Presets, InvalidUsageError



VALIDATED: bool = False



def package_installed(package: str) -> tuple[bool, list]:
    package_name = package.split('==')[0].strip()
    try:
        importlib.import_module(package_name)
        return True, []
    except ImportError:
        if package_name.startswith('google'):
            return (
                False, 
                [
                    'google-api-python-client==1.7.9',
                    'google-auth-httplib2==0.0.3',
                    'google-auth-oauthlib==0.4.0'
                ]
            )
        if package_name.startswith('apiclient'):
            return (
                False,
                ['apiclient==1.0.4']
            )
        if package_name.startswith('cryptography'):
            return (
                False,
                ['pycryptodome cryptography']
            )
        return (
            False,
            [package_name]
        )


def install_package(package: str) -> None:
    subprocess.run([pip_executable(), "-q", "--quiet", "install", package])


def pip_executable() -> str:
    return subprocess.run(["which", "pip"], capture_output=True, text=True).stdout.strip()


def find_missing_packages(packages: list[str]) -> list[str]:
    missing_packages: list[str] = []
    for package in packages:
        installed, modules = package_installed(package)
        if not installed:
            missing_packages += modules
    return list(set(missing_packages))


def ensure_packages_installed(packages: list[str]) -> None:
    global VALIDATED
    NEWLINE, TAB = '\n', '\t'
    if VALIDATED:
        return
    missing_packages = find_missing_packages(packages)
    if missing_packages:
        print(f'{NEWLINE}Package Manager:')
        join_str: str = f'{NEWLINE}{TAB}  '
        print(f"\tWARNING: missing packages detected:{NEWLINE}{TAB}  {join_str.join(missing_packages)}{NEWLINE}")
        response = input(f" > Ask Package Manager to install these packages automatically (Y/n)? ")
        if response.lower() in ['y', 'yes', 'ye', 'yeah', 'sure', 'ok']:
            for package in missing_packages:
                print(f"{NEWLINE}Package Manager: Installing {package} ...")
                install_package(package)
                print(f' > {package} installed successfully')
            print("Package Manager: Packages successfully installed. Please run main.py again.")
            VALIDATED = True
            sys.exit(0)
        else:
            print("Package Manager: Please install the required packages manually.")
            sys.exit(1)


def load_required_packages() -> None:
    global VALIDATED
    if VALIDATED:
        return
    if not os.path.exists(Presets.REQUIRED_PACKAGES_FILENAME):
        print(f'\nPackage Manager: \n\tERROR: "{Presets.REQUIRED_PACKAGES_FILENAME}" cannot be found. Expected file with required packages but file is missing.\n')
        exit(1)
    with open(Presets.REQUIRED_PACKAGES_FILENAME, 'r') as f:
        packages = [
            package for package in f.read().splitlines() \
                if package not in ['', ' ', '\t']
        ]
    ensure_packages_installed(packages)



if __name__ == '__main__':
    raise InvalidUsageError("This file should not be run. Only import this file and its contents. Do not run this file directly.")
load_required_packages()
