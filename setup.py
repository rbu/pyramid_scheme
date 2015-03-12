#!/usr/bin/env python
# encoding: utf8

from setuptools import setup

tests_require=[
    'pyexpect',
],

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
    tests_require=tests_require,
    extras_require = dict(
        testing=tests_require,
    ),
)
