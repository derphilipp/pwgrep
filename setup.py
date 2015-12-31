#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup
import os


def _read(fn):
    path = os.path.join(os.path.dirname(__file__), fn)
    return open(path).read()

setup(
        name='pwgrep',
        version='0.0.1',
        description='grep clone',
        author='Philipp Weißmann',
        author_email='mail@philipp-weissmann.de',
        url='https://github.com/derphilipp/pwgrep',
        license='MIT',
        platforms='ALL',
        long_description=_read('README.rst'),
        packages=[
            'pwgrep',
            ],
        include_package_data=True,
        install_requires=[
            'argparse'
            ],
        entry_points={
            'console_scripts': [
                #'pwgrep = pwgrep.ui:main'
                ]
            },
        classifiers=[
            'Programming Language :: Python :: 2.7 :: Only',
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: MIT License',
            'Topic :: Utilities'
            ]
        )

