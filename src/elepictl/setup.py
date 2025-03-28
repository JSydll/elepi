from setuptools import setup, find_packages

setup(
    name="elepictl",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'elepictl = elepictl.cli:main',
            'elepid = elepictl.daemon:main',
        ],
    },
    install_requires=[
        'python3-pydbus'
    ],
)