import os
from setuptools import setup, find_packages


setup(
    name = "sink",
    version = "1.0.0",
    platforms = ['Linux'],
    packages=find_packages(),
    install_requires=[
        'dropbox',
        'shell',
        'argparse',
        'sys',
        'termcolor'],
    url="https://github.com/kyle-verhoog/sink"
    )
