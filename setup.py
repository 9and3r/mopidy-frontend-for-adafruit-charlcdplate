from __future__ import unicode_literals

import re

from setuptools import find_packages, setup


def get_version(filename):
    with open(filename) as fh:
        metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", fh.read()))
        return metadata['version']


setup(
    name='Mopidy-Frontend-For-Adafruit-CharLCDPlate',
    version=get_version('mopidy_frontend-for-adafruit-charlcdplate/__init__.py'),
    url='https://github.com/9and3r/mopidy-frontend-for-adafruit-charlcdplate',
    license='Apache License, Version 2.0',
    author='Ander Orbegozo',
    author_email='9and3r@gmail.com',
    description='Extension to display info in Adafruit 16x2 LCD and control using the keypad',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
        'Mopidy >= 1.0',
        'Pykka >= 1.1',
    ],
    entry_points={
        'mopidy.ext': [
            'frontend-for-adafruit-charlcdplate = mopidy_frontend-for-adafruit-charlcdplate:Extension',
        ],
    },
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
)
