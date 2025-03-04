"""
packages.py

This module provides an abstraction for managing packages using the DNF package manager.
It includes methods to check if a package is installed and to install or remove packages.

"""
import subprocess

class PackageManager:
    """
    Simple interface to the DNF package manager allowing for easier testing.
    """

    @staticmethod
    def is_installed(package_name: str) -> bool:
        result = subprocess.run(
            ['dnf', 'list', '--installed', package_name],
            stdout=subprocess.DEVNULL
        )
        return result.returncode == 0

    @staticmethod
    def install(package_path: str) -> None:
        subprocess.run(['dnf', 'install', '-y', package_path],
                       check=True, stdout=subprocess.DEVNULL)


    @staticmethod
    def remove(package_name: str) -> None:
        subprocess.run(['dnf', 'remove', '-y', package_name],
                       check=True, stdout=subprocess.DEVNULL)
