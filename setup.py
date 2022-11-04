
from setuptools import setup, find_packages
import glob, os

setup(
    name='brace_lang',
    version='0.0.1',
    author='Anonymous',
    author_email='',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=[],
    entry_points={'console_scripts': []},
)
