#!/usr/bin/env python
# encoding: utf8

from setuptools import setup

setup(
    name='pyramid_scheme',
    version='1.0.0',
    description='Pyramid Helpers',
    author='Robert Buchholz, Felix Schwarz, Martin Häcker',
    author_email='rbu@rbu.sh',
    license='MIT',
    py_modules=['pyramid_scheme'],
    test_suite="pyramid_scheme",
    install_requires=[
        'pyramid',
        'requests',
        'future',
    ],
    tests_require=[
        'pyexpect',
    ]
)
