#!/usr/bin/env python

import os

from setuptools import setup

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def read(fname):
    return open(os.path.join(ROOT_DIR, fname)).read()


with open('requirements.txt') as reqs:
    requirements = [line.strip().split("==")[0] for line in reqs.readlines()]

setup(name='orco',
      version="0.4.0",
      description='Organized Computing',
      author='Stanislav Bohm',
      url='http://github.com/spirali/orco',
      packages=["orco", "orco.internals"],
      install_requires=requirements,
      package_data={'orco': ['static/*.gz', "static/js/*.gz", "static/css/*.gz"]},
      classifiers=("Programming Language :: Python :: 3",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent"))
