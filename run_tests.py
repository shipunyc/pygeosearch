"""
Runs all unit tests.
"""

import unittest

import tests.test_geohashsearch as test_geohashsearch
import tests.test_geosearch as test_geosearch


all_test_classes = [
  test_geohashsearch.TestAllFunctions,
  test_geosearch.TestAllFunctions
]

for test_class in all_test_classes:
  suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
  unittest.TextTestRunner(verbosity=2).run(suite)
