#!/usr/bin/python3

import unittest
import sys
import os

suite = unittest.TestSuite()
suite.addTest(unittest.TestLoader().discover('util/test/'))
suite.addTest(unittest.TestLoader().discover('ant/test/'))
runner = unittest.TextTestRunner()
result = runner.run(suite)
exit(0 if result.wasSuccessful() else 1)
