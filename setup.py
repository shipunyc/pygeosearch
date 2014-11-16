#!/usr/bin/env python

from distutils.core import setup
import setuptools

setup(name='pygeosearch',
      version='0.0.1',
      description='Geo search using redis',
      author="Pu Shi",
      author_email="mr.pu.shi@gmail.com",
      maintainer="Pu Shi",
      maintainer_email="mr.pu.shi@gmail.com",
      url="https://github.com/shipunyc/pygeosearch",
      py_modules=['geosearch'],
      packages=['pygeosearch'])
