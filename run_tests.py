#!/usr/bin/python3

import unittest

loader = unittest.TestLoader()
suite = loader.discover('./test')
runner = unittest.TextTestRunner()
runner.run(suite)
