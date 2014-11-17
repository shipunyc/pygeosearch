#!/usr/bin/env python

from distutils.core import setup
import setuptools


def discover_and_run_tests():
    import os
    import sys
    import unittest

    # get setup.py directory
    setup_file = sys.modules['__main__'].__file__
    setup_dir = os.path.abspath(os.path.dirname(setup_file))

    # use the default shared TestLoader instance
    test_loader = unittest.defaultTestLoader

    # use the basic test runner that outputs to sys.stderr
    test_runner = unittest.TextTestRunner()

    # automatically discover all tests
    # NOTE: only works for python 2.7 and later
    test_suite = test_loader.discover(setup_dir)

    # run the test suite
    test_runner.run(test_suite)

try:
    from setuptools.command.test import test

    class PyTest(test):

        def finalize_options(self):
            test.finalize_options(self)
            self.test_args = []
            self.test_suite = True

        def run_tests(self):
            discover_and_run_tests()

except ImportError:
    from distutils.core import Command

    class PyTest(Command):
        user_options = []

        def initialize_options(self):
                pass

        def finalize_options(self):
            pass

        def run(self):
            discover_and_run_tests()


setup(name='pygeosearch',
      version='0.0.2',
      description='Geo search using redis',
      author="Pu Shi",
      author_email="mr.pu.shi@gmail.com",
      maintainer="Pu Shi",
      maintainer_email="mr.pu.shi@gmail.com",
      url="https://github.com/shipunyc/pygeosearch",
      packages=['pygeosearch'],
      cmdclass={'test': PyTest},
      classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'
      ],
      install_requires=[
        'python-geohash==0.8.5',
        'redis==2.10.3'
      ])
