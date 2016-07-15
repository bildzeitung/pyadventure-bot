#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='scottadams',
    description='Scott Adams Adventureland! Engine',
    author='bildzeitung',
    author_email='bildzeitung@gmail.com',
    url='http://casa.blan.ca',
    packages=find_packages(exclude=["tests"]),
    test_suite='nose.collector',
    install_requires=[
        'click',
        'sqlalchemy',
    ],
    entry_points={
        'console_scripts': ['adventure=cli:main'],
    },
    include_package_data=True,
    package_data={
        'game_binaries': ['assets/*.dat'],
    },
)
