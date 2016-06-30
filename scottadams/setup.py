#!/usr/bin/env python

import os

from setuptools import setup, find_packages

setup(
    name='scottadams',
    description='Scott Adams Adventureland! Engine',
    author='bildzeitung',
    author_email='bildzeitung@gmail.com',
    url='http://casa.blan.ca',
    packages=find_packages(exclude=["tests"]),
    test_suite='nose.collector',
    setup_requires=['vcversioner'],
    install_requires=[
        'click',
    ],
    tests_require=[
    ],
    vcversioner={
        'root': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'),
        'version_module_paths': ['lib/_version.py'],
    },
    entry_points={
        'console_scripts': ['adventure=cli:main'],
    },
    include_package_data=True,
    package_data={
        'game_binaries': ['assets/*.dat'],
    },
)
